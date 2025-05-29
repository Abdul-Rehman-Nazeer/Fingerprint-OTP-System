import random
import string
from datetime import datetime, timedelta
import pywhatkit as kit
import os
import json

class OTPHandler:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.otp_db = {}
        
    def generate_otp(self):
        """Generate a random 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
        
    def send_otp_whatsapp(self, phone_number, otp):
        """Send OTP via WhatsApp"""
        try:
            # Remove any spaces or special characters from phone number
            phone_number = phone_number.replace('+', '').replace(' ', '')
            
            # Send WhatsApp message
            kit.sendwhatmsg_instantly(
                phone_no=f"+{phone_number}",
                message=f"Your OTP for fingerprint verification is: {otp}. Valid for 5 minutes.",
                wait_time=10
            )
            return True
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False
            
    def create_otp(self, user_id, phone=None):
        """Create and send OTP to user via WhatsApp"""
        otp = self.generate_otp()
        expiry = datetime.now() + timedelta(minutes=5)
        
        # Store OTP
        self.otp_db[user_id] = {
            'otp': otp,
            'expiry': expiry.isoformat()
        }
        
        # Send OTP via WhatsApp
        success = False
        if phone:
            if self.send_otp_whatsapp(phone, otp):
                success = True
                
        return success
        
    def verify_otp(self, user_id, entered_otp):
        """Verify the entered OTP"""
        if user_id not in self.otp_db:
            return False
            
        stored_data = self.otp_db[user_id]
        expiry = datetime.fromisoformat(stored_data['expiry'])
        
        if datetime.now() > expiry:
            del self.otp_db[user_id]
            return False
            
        return stored_data['otp'] == entered_otp 