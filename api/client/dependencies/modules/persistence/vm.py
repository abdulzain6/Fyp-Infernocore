import winreg
import subprocess

class VM:
    def __init__(self) -> None:
        try:
            self.process = subprocess.check_output(
                ['wmic', 'process', 'get', 'name'],
                text=True,  # Ensures output is in string format
                stderr=subprocess.STDOUT  # Redirect stderr to stdout
            )
        except Exception:
            self.process = ""
        self.process_list = [proc.strip() for proc in self.process.split('\n') if proc]

    def _enum_keys(self, reg):
        if not reg:
            return False
        keys = []
        try:
            i = 0
            while True:
                name = winreg.EnumKey(reg, i)
                keys.append(name)
                i += 1
        except WindowsError as e:
            return keys

    def _check_processes(self, exe, vm = False):
        return bool(exe in self.process_list and vm)

    def _hyperv_scan(self, microsoft, services):
        return "Hyper-V" in microsoft or "VirtualMachine" in microsoft

    def _vmware_scan(self, services, luid):
        vmware_svc = ['vmdebug', 'vmmouse', 'VMTools', 'VMMEMCTL']
        for s in vmware_svc:
            if s in services:
                return True
        if luid:
            iD = winreg.QueryValueEx(luid, 'Identifier')
            if 'vmware' in str(iD[0]).lower():
                return True
        return False

    def _virtualpc_scan(self, services):
        virtpc_svc = ['vpcbus', 'vpc-s3', 'vpcuhub', 'msvmmouf']
        return any(s in services for s in virtpc_svc)

    def _sunvirtual_scan(self, services, luid, dsys, dsdtkey, fadtkey):
        virtpc_svc = ['VBoxMouse', 'VBoxGuest', 'VBoxService', 'VBoxSF']
        for s in virtpc_svc:
            if s in services:
                return True
        if luid:
            iD = winreg.QueryValueEx(luid, 'Identifier')
            if 'vbox' in str(iD[0]).lower():
                return True
        if dsys:
            sysbios = winreg.QueryValueEx(dsys, 'SystemBiosVersion')
            if 'vbox' in str(sysbios[0]).lower():
                return True
        if "VBOX__" in dsdtkey or "VBOX__" in fadtkey:
            return True
        return False

    def _xen_scan(self, services, dsdtkey, fadtkey, rsdtkey):
        virtpc_svc = ['xenevtchn', 'xennet', 'xennet6', 'xensvc', 'xenvdb']
        for s in virtpc_svc:
            if s in services:
                return True
        if "Xen" in dsdtkey or "Xen" in fadtkey or "Xen" in rsdtkey:
            return True
        return False

    def _qemu_kvm_scan(self, luid, sycp):
        if luid:
            iD = winreg.QueryValueEx(luid, 'Identifier')
            if 'qemu' in str(iD[0]).lower():
                return True
        if sycp:
            cp = winreg.QueryValueEx(sycp, 'ProcessorNameString')
            if 'qemu' in str(cp[0]).lower():
                return True
        return False

    def _find_luid(self):
        n = 0
        luid = False
        for i in range(4):
            while n < 4:
                try:
                    luid = winreg.OpenKey(
                        winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port %i\\Scsi Bus %i\\Target Id 0\\Logical Unit Id 0' % (i, n))
                    break
                except Exception:
                    n += 1
        return luid

    def _try_openkey(self, path):
        try:
            return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        except Exception as e:
            return False

    def _open_keys(self, path: dict):
        return {v: self._try_openkey(k) for k, v in path.items()}

    def _enum_many_keys(self, keys: dict):
        return {k: self._enum_keys(v) for k, v in keys.items()}

    def is_vm(self):
        paths = {'SOFTWARE\\Microsoft': "micr", 
                 'HARDWARE\\ACPI\\DSDT': "dsdt", 
                 'HARDWARE\\ACPI\\FADT': "fadt", 
                 'HARDWARE\\ACPI\\RSDT': "rsdt", 
                 'HARDWARE\\DESCRIPTION\\System': "dsys", 
                 'SYSTEM\\ControlSet001\\Services': "srvc", 
                 'HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0': "sycp"}

        keys = self._open_keys(paths)

        luid = self._find_luid()

        dsys = self._try_openkey('HARDWARE\\DESCRIPTION\\System')

        sycp = self._try_openkey(
            'HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0')

        enumerated_keys = self._enum_many_keys(keys)

        vm = self._xen_scan(enumerated_keys["srvc"], enumerated_keys["dsdt"], 
                            enumerated_keys["fadt"], enumerated_keys["rsdt"])

        if not vm:
            vm = self._vmware_scan(enumerated_keys["srvc"], luid)
        if not vm:
            vm = self._hyperv_scan(
                enumerated_keys["micr"], enumerated_keys["srvc"])
        if not vm:
            vm = self._qemu_kvm_scan(luid, sycp)
        if not vm:
            vm = self._virtualpc_scan(enumerated_keys["srvc"])
        if not vm:
            vm = self._sunvirtual_scan(
                enumerated_keys["srvc"], luid, dsys, enumerated_keys["dsdt"], enumerated_keys["fadt"])
        if not vm:
            vm = self._check_processes("vmwareuser.exe", 'VMware')
        if not vm:
            vm = self._check_processes("vmwaretray.exe", 'VMware')
        if not vm:
            vm = self._check_processes("vmusrvc.exe", 'VirtualPC')
        if not vm:
            vm = self._check_processes("vmsrvc.exe", 'VirtualPC')
        if not vm:
            vm = self._check_processes("vboxservice.exe", 'Sun VirtualBox')
        if not vm:
            vm = self._check_processes("vboxtray.exe", 'Sun VirtualBox')
        if not vm:
            vm = self._check_processes("xenservice.exe", 'Xen')

        return vm

if __name__ == "__main__":
    vm = VM()
    print(vm.is_vm())