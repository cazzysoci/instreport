import requests
import time
import random
import argparse
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class InstagramReporter:
    def __init__(self, target_username, reason, proxy_file=None, threads=10):
        self.target_username = target_username
        self.reason = reason
        self.threads = threads
        self.success_count = 0
        self.fail_count = 0
        self.proxies = []
        
        # Load proxies if provided
        if proxy_file:
            try:
                with open(proxy_file, 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip()]
                print(f"{Fore.GREEN}[+] Loaded {len(self.proxies)} proxies")
            except Exception as e:
                print(f"{Fore.RED}[!] Error loading proxy file: {e}")
        
        # Report reasons mapping
        self.report_reasons = {
            "spam": "1",
            "violence": "2", 
            "harassment": "3",
            "suicide": "4",
            "hate_speech": "5",
            "illegal_content": "6",
            "intellectual_property": "7",
            "bullying": "8",
            "scam": "9",
            "false_information": "10"
        }
        
        # Check if reason is valid
        if reason not in self.report_reasons:
            print(f"{Fore.RED}[!] Invalid reason. Available reasons: {', '.join(self.report_reasons.keys())}")
            exit(1)
            
    def get_random_proxy(self):
        """Get a random proxy from the loaded proxy list"""
        if not self.proxies:
            return None
        proxy = random.choice(self.proxies)
        return {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        
    def get_random_user_agent(self):
        """Generate a random user agent"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0",
            "Mozilla/5.0 (Android 11; Mobile; LG-M255; rv:88.0) Gecko/88.0 Firefox/88.0",
        ]
        return random.choice(user_agents)
        
    def report_user(self, thread_id):
        """Report an Instagram user"""
        # In a real implementation, this would use Instagram's API or simulate browser behavior
        # This is a mock implementation for educational purposes only
        
        headers = {
            "User-Agent": self.get_random_user_agent(),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "https://www.instagram.com",
            "Connection": "keep-alive",
            "Referer": f"https://www.instagram.com/{self.target_username}/",
        }
        
        # Mock API endpoint (in a real implementation, this would be Instagram's actual report endpoint)
        url = f"https://www.instagram.com/users/{self.target_username}/report/"
        
        try:
            # Get a random proxy if available
            proxy = self.get_random_proxy()
            
            # Simulate reporting (this is a mock)
            time.sleep(random.uniform(1, 3))  # Random delay to avoid detection
            
            # In a real implementation, this would be a POST request with proper authentication and parameters
            # Here we're just simulating success/failure for educational purposes
            report_success = random.random() > 0.2  # 80% success rate for demonstration
            
            if report_success:
                self.success_count += 1
                print(f"{Fore.GREEN}[+] Thread {thread_id}: Successfully reported {self.target_username} - Reason: {self.reason}")
            else:
                self.fail_count += 1
                print(f"{Fore.RED}[-] Thread {thread_id}: Failed to report {self.target_username}")
                
            return report_success
            
        except Exception as e:
            self.fail_count += 1
            print(f"{Fore.RED}[!] Thread {thread_id}: Error reporting {self.target_username}: {str(e)}")
            return False
            
    def start_attack(self):
        """Start the reporting attack with multiple threads"""
        print(f"{Fore.CYAN}[*] Starting report attack on {self.target_username}")
        print(f"{Fore.CYAN}[*] Reason: {self.reason}")
        print(f"{Fore.CYAN}[*] Threads: {self.threads}")
        print(f"{Fore.YELLOW}[*] Press Ctrl+C to stop the attack")
        
        try:
            with ThreadPoolExecutor(max_workers=self.threads) as executor:
                # Create an infinite loop for continuous reporting
                thread_id = 0
                while True:
                    thread_id += 1
                    executor.submit(self.report_user, thread_id)
                    
                    # Print stats every 10 reports
                    if thread_id % 10 == 0:
                        print(f"{Fore.BLUE}[*] Stats: {self.success_count} successful reports, {self.fail_count} failed")
                    
                    # Small delay between spawning threads
                    time.sleep(0.5)
                    
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}[*] Attack stopped by user")
            print(f"{Fore.GREEN}[+] Final stats: {self.success_count} successful reports, {self.fail_count} failed")

def main():
    parser = argparse.ArgumentParser(description="Instagram Maximum Report Tool")
    parser.add_argument("-u", "--username", required=True, help="Target Instagram username")
    parser.add_argument("-r", "--reason", required=True, 
                        choices=["spam", "violence", "harassment", "suicide", "hate_speech", 
                                "illegal_content", "intellectual_property", "bullying", "scam", "false_information"],
                        help="Reason for reporting")
    parser.add_argument("-p", "--proxy", help="Path to proxy file (optional)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads (default: 10)")
    
    args = parser.parse_args()
    
    print(f"{Fore.CYAN}='='='='='='='='='='='='='='='='='='='='='=")
    print(f"{Fore.CYAN}|    Instagram Max Report Tool    |")
    print(f"{Fore.CYAN}|    BY CAZZYSOCI PH              |")
    print(f"{Fore.CYAN}='='='='='='='='='='='='='='='='='='='='='=")
    print(f"{Fore.YELLOW}[!] Disclaimer: This tool is for educational purposes only")
    print(f"{Fore.YELLOW}[!] Misuse of this tool may violate Instagram's Terms of Service")
    print(f"{Fore.YELLOW}[!] The author is not responsible for any misuse or damage")
    print()
    
    reporter = InstagramReporter(args.username, args.reason, args.proxy, args.threads)
    reporter.start_attack()

if __name__ == "__main__":
    main()
