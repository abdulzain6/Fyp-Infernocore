from ..scripting_interface import execute_powershell_script
from ...scripts.powershell_scripts.system import getAccounts, createAccountScript
import processManagement

class Account:
    @staticmethod
    def get_accounts():
        accounts = []
        data = execute_powershell_script(getAccounts, True).split("\n\r\n")
        for i, account in enumerate(data, start=1):
            account_dict = {}
            acc_split = account.split("\n")
            for d in acc_split:
                if "Name" in d and "FullName" not in d:
                    account_dict["Name"] = d.replace("Name        : ", "").strip()
                elif "AccountType" in d:
                    account_dict["AccountType"] = d.replace("AccountType : ", "").strip()
                elif "Caption" in d:
                    account_dict["Caption"] = d.replace("Caption     : ", "").strip()
                elif "Domain" in d:
                    account_dict["Domain"] = d.replace("Domain      : ", "").strip()
                elif "SID" in d:
                    account_dict["SID"] = d.replace("SID         : ", "").strip()
                elif "FullName" in d:
                    account_dict["FullName"] = d.replace("FullName    :", "").strip()
            account_dict["id"] = i
            accounts.append(account_dict)
            
        return accounts

    @staticmethod
    def create_account(name, password, full_name, description):
        if processManagement.isElevated() != 1:
            return 0
        return execute_powershell_script(createAccountScript.format(password, name, full_name, description, name), getOutput=True)
