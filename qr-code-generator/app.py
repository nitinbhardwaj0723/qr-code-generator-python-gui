import tkinter as tk
from tkinter import filedialog, messagebox
import qrcode
from PIL import Image, ImageTk

# Global variables
qr_img = None
preview_photo = None


def generate_qr():
    global qr_img, preview_photo

    data = text_input.get("1.0", tk.END).strip()
    filename = filename_entry.get().strip()

    if not data:
        messagebox.showerror("Error", "Please enter text or URL!")
        return

    if not filename:
        filename = "qr_code"

    try:
        # QR generate
        qr = qrcode.QRCode(
            version=1,
            box_size=12,   # QR quality
            border=4
        )
        qr.add_data(data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Preview ko bada aur clear dikhane ke liye resize
        preview = qr_img.resize((300, 300), Image.LANCZOS)
        preview_photo = ImageTk.PhotoImage(preview)

        # Preview update
        preview_label.config(image=preview_photo, text="")
        preview_label.image = preview_photo  # important!

        status_label.config(text=f"QR Code Generated: {filename}.png", fg="green")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


def save_qr():
    global qr_img

    if qr_img is None:
        messagebox.showwarning("Warning", "Generate QR first!")
        return

    filename = filename_entry.get().strip()
    if not filename:
        filename = "qr_code"

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        initialfile=filename,
        filetypes=[("PNG files", "*.png")]
    )

    if file_path:
        qr_img.save(file_path)
        messagebox.showinfo("Success", f"QR Code saved successfully!\n{file_path}")
        status_label.config(text="QR Code Saved Successfully!", fg="blue")


def clear_all():
    global qr_img, preview_photo

    qr_img = None
    preview_photo = None

    text_input.delete("1.0", tk.END)
    filename_entry.delete(0, tk.END)
    filename_entry.insert(0, "qr_code")

    preview_label.config(image="", text="QR Preview Here")
    preview_label.image = None

    status_label.config(text="Cleared successfully.", fg="orange")


# Main window
root = tk.Tk()
root.title("Advanced QR Code Generator")
root.geometry("900x600")
root.resizable(False, False)
root.config(bg="#f0f4f8")

# Title
title = tk.Label(
    root,
    text="Advanced QR Code Generator",
    font=("Arial", 22, "bold"),
    bg="#f0f4f8",
    fg="#1f3c88"
)
title.pack(pady=15)

# Main frame
frame = tk.Frame(root, bg="white", bd=2, relief="groove")
frame.pack(padx=20, pady=10, fill="both", expand=True)

# Left frame
left_frame = tk.Frame(frame, bg="white")
left_frame.pack(side="left", padx=30, pady=20, fill="both", expand=True)

# Right frame
right_frame = tk.Frame(frame, bg="white")
right_frame.pack(side="right", padx=30, pady=20, fill="both", expand=True)

# Input label
input_label = tk.Label(left_frame, text="Enter Text / URL:", font=("Arial", 12, "bold"), bg="white")
input_label.pack(anchor="w")

# Text input
text_input = tk.Text(left_frame, width=40, height=10, font=("Arial", 11))
text_input.pack(pady=10)

# Filename label
filename_label = tk.Label(left_frame, text="File Name:", font=("Arial", 12, "bold"), bg="white")
filename_label.pack(anchor="w")

filename_entry = tk.Entry(left_frame, width=35, font=("Arial", 11))
filename_entry.pack(pady=10, ipady=5)
filename_entry.insert(0, "qr_code")

# Buttons
generate_btn = tk.Button(
    left_frame,
    text="Generate QR",
    font=("Arial", 12, "bold"),
    bg="#2563eb",
    fg="white",
    width=20,
    height=2,
    command=generate_qr
)
generate_btn.pack(pady=10)

save_btn = tk.Button(
    left_frame,
    text="Save QR",
    font=("Arial", 12, "bold"),
    bg="#16a34a",
    fg="white",
    width=20,
    height=2,
    command=save_qr
)
save_btn.pack(pady=10)

clear_btn = tk.Button(
    left_frame,
    text="Clear",
    font=("Arial", 12, "bold"),
    bg="#dc2626",
    fg="white",
    width=20,
    height=2,
    command=clear_all
)
clear_btn.pack(pady=10)

# Preview title
preview_title = tk.Label(right_frame, text="QR Preview", font=("Arial", 18, "bold"), bg="white")
preview_title.pack(pady=10)

# Preview frame
preview_box = tk.Frame(right_frame, bg="#e5e7eb", width=340, height=340, bd=2, relief="ridge")
preview_box.pack(pady=20)
preview_box.pack_propagate(False)

preview_label = tk.Label(
    preview_box,
    text="QR Preview Here",
    font=("Arial", 14),
    bg="#e5e7eb"
)
preview_label.pack(expand=True)

# Status label
status_label = tk.Label(
    right_frame,
    text="Ready to generate QR code.",
    font=("Arial", 11, "italic"),
    bg="white",
    fg="#444",
    wraplength=300
)
status_label.pack(pady=15)

# Footer
footer = tk.Label(
    root,
    text="Built with Python, Tkinter, qrcode, Pillow",
    font=("Arial", 10),
    bg="#f0f4f8",
    fg="#666"
)
footer.pack(pady=8)

root.mainloop()