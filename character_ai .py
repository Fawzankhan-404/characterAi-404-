from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
import speech_recognition as sr
import threading
import argparse
import pyttsx3
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Character mapping dictionary
CHARACTER_URLS = {
    "kabir singh": "https://character.ai/chat/1RUUBhQKZzc5tJxa3XmHxRN7vL4fbV0Nb6zPNnd2h9s",
    "majnu": "https://character.ai/chat/4hkrm_XSMOXLApqFulmz2JaDzVtjMlSvvviUTf7Yd8Y",
    "tony stark": "https://character.ai/chat/pe5AdTpnjL-r_pya0JoXXd1UMlYpiRiQ0bgzcxHJwrg",
    "jarvis": "https://character.ai/chat/1U5b4Nuuf3LnBLvAbaxUfllTYvttzWH2m4hjvj5ubfE"
}

class CharacterAI:
    def __init__(self):
        self.driver = None
        self.cookies_file = "character_ai_cookies.json"
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.mic_thread = None
        self.current_character = None
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
       
        
    def initialize_driver(self):
        """Initialize the Chrome WebDriver with necessary options"""
        chrome_options = Options()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        chrome_options.add_argument("--use-fake-device-for-media-stream")
        chrome_options.add_argument("--enable-media-stream")
        chrome_options.add_argument("--allow-file-access-from-files")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set window size
        self.driver.set_window_size(1920, 1080)
        
    def save_cookies(self):
        """Save cookies to file"""
        if self.driver:
            cookies = self.driver.get_cookies()
            with open(self.cookies_file, 'w') as f:
                json.dump(cookies, f)
                
    def load_cookies(self):
        """Load cookies from file"""
        if os.path.exists(self.cookies_file):
            with open(self.cookies_file, 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            return True
        return False
        
    def login(self):
        """Handle login process"""
        try:
            print("Starting login process...")
            self.driver.get("https://character.ai/")
            time.sleep(3)
            
            try:
                login_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign in')]"))
                )
                login_button.click()
                time.sleep(2)
            except Exception as e:
                print(f"Error clicking login button: {e}")
                return False

            try:
                google_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Google') or contains(., 'google')]"))
                )
                google_button.click()
                time.sleep(3)
            except Exception as e:
                print(f"Error clicking Google button: {e}")
                return False

            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(3)

            try:
                email_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
                )
                email_input.clear()
                email_input.send_keys("yourgmail") #use fake or new account
                time.sleep(1)
                email_input.send_keys(Keys.RETURN)
                time.sleep(3)
            except Exception as e:
                print(f"Error entering email: {e}")
                return False

            try:
                password_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
                )
                password_input.clear()
                password_input.send_keys("addyourpass") 
                time.sleep(1)
                password_input.send_keys(Keys.RETURN)
                time.sleep(5)
            except Exception as e:
                print(f"Error entering password: {e}")
                return False

            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(5)

            self.driver.get("https://character.ai/")
            time.sleep(5)
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder*='Message']"))
                )
                return True
            except:
                print("Could not load chat page. Please check if you need to log in manually...")
                time.sleep(10)
                return True
                
        except Exception as e:
            print(f"Error during login: {e}")
            return False
        
    def select_character(self, character_name):
        """Select a specific character to chat with"""
        try:
            character_name = character_name.lower()
            if character_name in CHARACTER_URLS:
                print(f"Navigating to {character_name}'s chat...")
                self.driver.get(CHARACTER_URLS[character_name])
                self.current_character = character_name
                time.sleep(3)
                
                # Wait for chat interface to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder='Type a message']"))
                )
                return True
            else:
                print(f"Character '{character_name}' not found. Available characters:")
                for char in CHARACTER_URLS.keys():
                    print(f"- {char}")
                return False
        except Exception as e:
            print(f"Error selecting character: {e}")
            return False
            
    def send_message(self, message):
        """Send a message to the character"""
        try:
            # Wait for input field to be present using the correct selector
            input_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder*='Message']"))
            )
            input_field.clear()
            input_field.send_keys(message)
            time.sleep(1)
            input_field.send_keys(Keys.RETURN)
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
            
    def speak_response(self, text):
        """Speak the AI's response"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error speaking response: {e}")

    def get_character_response(self, timeout=30):
        """Get the character's response using multiple XPath patterns"""
        try:
            response_patterns = [
              #  "//div[contains(@class, 'swiper-slide-active')]//div[contains(@class, 'message-text')]//p",
                "/html/body/div[1]/div/main/div/div/div/main/div/div[1]/div[2]/div/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]",
                "/html/body/div[1]/div/main/div/div/div/main/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[2]/div/div[1]/p"
            ]
            
            for pattern in response_patterns:
                try:
                    response_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, pattern))
                    )
                    if response_element and response_element.text.strip():
                        response_text = response_element.text.strip()
                        return response_text
                    self.speak_response(response_text)
                        
                except:
                    continue
            
            response_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".swiper-slide-active .message-text p"))
            )
            response_text = response_element.text.strip()
            if character_ai_interaction(chat_mode=False):
                return response_text
            self.speak_response(response_text)
            
            
        except Exception as e:
            print(f"Error getting response: {str(e)}")
            return None
            
    def start_chat(self, character_name=None):
        """Start a chat session with a character"""
        try:
            self.initialize_driver()
            if self.login():
                if character_name:
                    self.select_character(character_name)
                return True
            return False
        except Exception as e:
            print(f"Error starting chat: {e}")
            return False
            
    def close(self):
        """Close the browser and clean up"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def handle_call_command(self):
        """Handle the call button click"""
        try:
            call_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/main/div/div/div/main/div/div[1]/div[2]/div/div[2]/div/div/button"))
            )
            call_button.click()
            print("Call initiated...")
            return True
        except Exception as e:
            print(f"Error initiating call: {str(e)}")
            return False

    def handle_hangup_command(self):
        """Handle the hang up button click"""
        try:
            hangup_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/main/div/div/div/main/div[2]/div/div[3]/div[2]/button"))
            )
            hangup_button.click()
            print("Call ended...")
            return True
        except Exception as e:
            print(f"Error ending call: {str(e)}")
            return False

    def start_voice_listening(self):
        """Start listening for voice commands"""
        if self.is_listening:
            return
        
        self.is_listening = True
        self.mic_thread = threading.Thread(target=self._listen_for_commands)
        self.mic_thread.daemon = True
        self.mic_thread.start()
        print("Voice command listening started...")

    def stop_voice_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        if self.mic_thread:
            self.mic_thread.join()
        print("Voice command listening stopped...")

    def _listen_for_commands(self):
        """Background thread for listening to voice commands"""
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    
                try:
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"Voice command detected: {command}")
                    
                    # Process voice commands
                    if command in ["call", "start call"]:
                        self.handle_call_command()
                    elif command in ["hang up", "hangup", "cut", "end call"]:
                        self.handle_hangup_command()
                    elif command in ["stop listening", "stop voice"]:
                        self.stop_voice_listening()
                    else:
                        # Treat as regular message
                        self.send_message(command)
                        response = self.get_character_response()
                        if response:
                            print(f"AI: {response}")
                            
                except sr.UnknownValueError:
                    pass  # Ignore unrecognized speech
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                    
            except Exception as e:
                print(f"Error in voice recognition: {e}")
                time.sleep(1)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Character AI Interaction')
    parser.add_argument('-c', '--chat', action='store_true', help='Run in chat mode (default is voice mode)')
    parser.add_argument('-n', '--name', type=str, help='Character name to chat with')
    parser.add_argument('-l', '--list', action='store_true', help='List available characters')
    parser.add_argument('-s', '--speak', action='store_true', help='Enable text-to-speech for responses')
    return parser.parse_args()

def character_ai_interaction(character_name=None, chat_mode=False, speak_mode=False):
    """Main interaction function that can be imported and used in Jarvis"""
    print("Initializing Character AI interaction...")
    ai = CharacterAI()
    try:
        if ai.start_chat(character_name):
            if not chat_mode:
                print("\nRunning in VOICE MODE")
                print("Voice commands available:")
                print("- 'call' or 'start call' to initiate a call")
                print("- 'hang up', 'hangup', 'cut', or 'end call' to end a call")
                print("- 'stop listening' or 'stop voice' to stop voice commands")
                print("- 'switch character' to change characters")
                print("- Any other speech will be sent as a message")
                ai.start_voice_listening()
            else:
                print("\nRunning in CHAT MODE")
                print("Type your messages or commands:")
                print("- 'call' or 'start call' to initiate a call")
                print("- 'hang up', 'hangup', 'cut', or 'end call' to end a call")
                print("- 'switch character' to change characters")
                print("- 'exit', 'quit', or 'stop' to end the session")
            
            print("\nText-to-speech is " + ("ENABLED" if speak_mode else "DISABLED"))
            
            while True:
                user_input = input("You: ").strip().lower()
                
                if user_input in ["exit", "quit", "stop"]:
                    break
                
                if user_input == "switch character" or user_input == "switch ch":
                    print("\nAvailable characters:")
                    for char in CHARACTER_URLS.keys():
                        print(f"- {char}")
                    new_character = input("Enter character name: ").strip().lower()
                    if new_character in CHARACTER_URLS:
                        ai.select_character(new_character)
                    else:
                        print("Invalid character name!")
                    continue
                
                if user_input in ["call", "start call"]:
                    ai.handle_call_command()
                    continue
                
                if user_input in ["hang up", "hangup", "cut", "end call"]:
                    ai.handle_hangup_command()
                    continue
                
                if not chat_mode:
                    if user_input in ["start voice", "start listening"]:
                        ai.start_voice_listening()
                        continue
                        
                    if user_input in ["stop voice", "stop listening"]:
                        ai.stop_voice_listening()
                        continue
                    
                if ai.send_message(user_input):
                    response = ai.get_character_response()
                    if response:
                        print(f"AI: {response}")
                        if speak_mode:
                            ai.speak_response(response)
                    else:
                        print("No response received from the AI.")
                        
    except Exception as e:
        print(f"Error in character AI interaction: {e}")
    finally:
        if not chat_mode:
            ai.stop_voice_listening()
        ai.close()
        print("Browser closed.")

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()
    
    # List available characters if requested
    if args.list:
        print("\nAvailable characters:")
        for char in CHARACTER_URLS.keys():
            print(f"- {char}")
        exit(0)
    
    # Run in appropriate mode
    character_ai_interaction(character_name=args.name, chat_mode=args.chat, speak_mode=args.speak) 
    
