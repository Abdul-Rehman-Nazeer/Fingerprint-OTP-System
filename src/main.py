import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
from PIL import Image, ImageTk
import os
from fingerprint import FingerprintProcessor
from otp import OTPHandler

class FingerprintOTPSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Fingerprint OTP System")
        self.root.geometry("800x600")
        
        # Initialize components
        self.fp_processor = FingerprintProcessor()
        self.otp_handler = OTPHandler()
        
        # Create GUI elements
        self.create_gui()
        
    def create_gui(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Create tabs
        self.enroll_tab = ttk.Frame(notebook)
        self.verify_tab = ttk.Frame(notebook)
        
        notebook.add(self.enroll_tab, text='Enroll User')
        notebook.add(self.verify_tab, text='Verify User')
        
        self.setup_enroll_tab()
        self.setup_verify_tab()
        
    def setup_enroll_tab(self):
        # Frame for enrollment
        enroll_frame = ttk.Frame(self.enroll_tab, padding="10")
        enroll_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(enroll_frame, text="Enroll New User", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(enroll_frame, text="User ID:").grid(row=1, column=0, sticky=tk.W)
        self.enroll_user_id_entry = ttk.Entry(enroll_frame)
        self.enroll_user_id_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(enroll_frame, text="WhatsApp Number:").grid(row=2, column=0, sticky=tk.W)
        self.enroll_phone_entry = ttk.Entry(enroll_frame)
        self.enroll_phone_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.enroll_image_path = None
        self.enroll_browse_btn = ttk.Button(enroll_frame, text="Browse Fingerprint Image", command=self.browse_enroll_image)
        self.enroll_browse_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.enroll_status_label = ttk.Label(enroll_frame, text="")
        self.enroll_status_label.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.enroll_btn = ttk.Button(enroll_frame, text="Enroll User", command=self.enroll_user)
        self.enroll_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
    def setup_verify_tab(self):
        # Frame for verification
        verify_frame = ttk.Frame(self.verify_tab, padding="10")
        verify_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(verify_frame, text="Verify User", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(verify_frame, text="User ID:").grid(row=1, column=0, sticky=tk.W)
        self.verify_user_id_entry = ttk.Entry(verify_frame)
        self.verify_user_id_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.verify_image_path = None
        self.verify_browse_btn = ttk.Button(verify_frame, text="Browse Fingerprint Image", command=self.browse_verify_image)
        self.verify_browse_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Label(verify_frame, text="Enter OTP:").grid(row=3, column=0, sticky=tk.W)
        self.verify_otp_entry = ttk.Entry(verify_frame)
        self.verify_otp_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.generate_otp_btn = ttk.Button(verify_frame, text="Generate OTP", command=self.generate_otp)
        self.generate_otp_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        self.verify_status_label = ttk.Label(verify_frame, text="")
        self.verify_status_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.verify_btn = ttk.Button(verify_frame, text="Verify User", command=self.verify_user)
        self.verify_btn.grid(row=6, column=0, columnspan=2, pady=10)
        
    def browse_enroll_image(self):
        initial_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'datasets')
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Select Fingerprint Image for Enrollment",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tif")] # Added .tif
        )
        if file_path:
            self.enroll_image_path = file_path
            self.enroll_status_label.config(text=f"Image selected: {os.path.basename(file_path)}")
            
    def browse_verify_image(self):
        initial_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'datasets')
        file_path = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Select Fingerprint Image for Verification",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tif")] # Added .tif
        )
        if file_path:
            self.verify_image_path = file_path
            self.verify_status_label.config(text=f"Image selected: {os.path.basename(file_path)}")
            
    def enroll_user(self):
        user_id = self.enroll_user_id_entry.get()
        phone = self.enroll_phone_entry.get()
        
        if not user_id or not phone or not self.enroll_image_path:
            messagebox.showerror("Error", "Please fill all fields and select an image.")
            return
            
        # Basic phone number validation (can be enhanced)
        if not phone.startswith('+') or len(phone) < 10:
             messagebox.showerror("Error", "Please enter a valid phone number with country code (e.g., +1234567890).")
             return
             
        # Process image and get descriptors
        image = cv2.imread(self.enroll_image_path)
        if image is None:
            messagebox.showerror("Error", "Failed to read image.")
            return
        
        processed_image = self.fp_processor.preprocess_fingerprint(image)
        keypoints, descriptors = self.fp_processor.extract_features(processed_image)
        
        if descriptors is None:
            messagebox.showerror("Error", "Could not extract features from image. Please try another image.")
            return
            
        # Store user and template
        # In a real system, you'd have a user database here. For now, let's simulate storage.
        # We need a simple way to associate user_id and phone with the template.
        # Let's add a simple user storage in FingerprintProcessor or main.
        
        # For now, let's assume we store user data directly with templates or in a simple dict
        # Let's modify FingerprintProcessor to handle user data too, or add a user_db here.
        # Adding a simple user_db here for demonstration.
        if not hasattr(self, 'user_data_db'):
            self.user_data_db = {}
            
        self.user_data_db[user_id] = {
            'phone': phone,
            # Add other potential user data here later
        }
        
        self.fp_processor.store_template(user_id, descriptors)
        
        messagebox.showinfo("Success", f"User {user_id} enrolled successfully!")
        self.enroll_status_label.config(text=f"Enrollment successful for {user_id}")
        
    def generate_otp(self):
        user_id = self.verify_user_id_entry.get()
        if not user_id:
            messagebox.showerror("Error", "Please enter User ID to generate OTP.")
            return
            
        # Retrieve phone number from stored user data
        if not hasattr(self, 'user_data_db') or user_id not in self.user_data_db:
             messagebox.showerror("Error", "User not found. Please enroll the user first.")
             return
             
        phone_number = self.user_data_db[user_id]['phone']

        # Generate and send OTP
        success = self.otp_handler.create_otp(user_id, phone=phone_number)
        
        if success:
            messagebox.showinfo("OTP Sent", f"OTP sent to WhatsApp for User ID: {user_id}")
        else:
            messagebox.showerror("OTP Failed", "Failed to send OTP. Ensure WhatsApp Web is open and phone number is correct.")
        
    def verify_user(self):
        user_id = self.verify_user_id_entry.get()
        entered_otp = self.verify_otp_entry.get()
        
        if not user_id or not entered_otp or not self.verify_image_path:
            messagebox.showerror("Error", "Please fill all verification fields and select an image.")
            return
            
        # Verify OTP first
        if not self.otp_handler.verify_otp(user_id, entered_otp):
            messagebox.showerror("Error", "Invalid or expired OTP.")
            self.verify_status_label.config(text="Verification failed: Invalid OTP")
            return
            
        # Verify fingerprint
        fingerprint_match = self.fp_processor.verify_fingerprint(user_id, self.verify_image_path)
        
        if fingerprint_match:
            messagebox.showinfo("Success", "Fingerprint and OTP verification successful!")
            self.verify_status_label.config(text="Verification successful!")
        else:
            messagebox.showerror("Error", "Fingerprint verification failed.")
            self.verify_status_label.config(text="Verification failed: Fingerprint mismatch")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = FingerprintOTPSystem(root)
    app.run() 