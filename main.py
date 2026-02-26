import tkinter as tk
from tkinter import ttk
from client.userClient import User
from config import Status

class MessengerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Messenger")
        self.root.geometry("900x550")

        self.user = None
        self.connected = False
        self.user_id = None
        self.conversations = {}

        self.recipient_id = None
        self.setup_ui()
        self.set_ui_enabled(False)

    # =========================
    # UI SETUP
    # =========================
    def setup_ui(self):
        self.build_top_bar()

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        self.left_frame = ttk.Frame(main_frame, width=200)
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.build_user_list()
        self.build_chat_area()

    def build_top_bar(self):
        top = ttk.Frame(self.root)
        top.pack(fill="x", padx=5, pady=5)

        ttk.Label(top, text="Your ID:").pack(side="left")

        self.id_entry = ttk.Entry(top, width=15)
        self.id_entry.pack(side="left", padx=5)

        ttk.Button(top, text="Connect", command=self.connect).pack(side="left", padx=5)

        self.status = ttk.Label(top, text="Not Connected", foreground="red")
        self.status.pack(side="left", padx=10)

    def set_ui_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.message_entry.config(state=state)
        self.new_user_entry.config(state=state)
        for w in self.user_buttons_frame.winfo_children():
            w.config(state=state)
    # =========================
    # CONNECT
    # =========================
    def connect(self):
        user_id = self.id_entry.get().strip()

        if not user_id.isdigit() or not (0 < int(user_id) < 256):
            self.status.config(text="Invalid ID", foreground="red")
            return

        self.user = User(int(user_id))

        if self.user.associate() == Status.ASSOCIATE_SUCCESS:
            self.connected = True
            self.status.config(
                text=f"Connected as {user_id}",
                foreground="green"
            )
            self.id_entry.config(state="disabled")
            self.set_ui_enabled(True)

            self.poll_messages()
                

    # =========================
    # POLLING LOOP
    # =========================
    def poll_messages(self):
        if not self.connected:
            return

        status, message, user_id = self.user.get()

        if status == Status.GOT_RESPONSE:
            self.add_message(user_id, str(user_id), message)
        elif status == Status.ASSOCIATE_FAIL:
            self.connected = False
            self.status.config(text="Disconnected", foreground="red")
            self.id_entry.config(state="normal")
            self.set_ui_enabled(False)
            self.root.after(1000, self.reconnect)
            return
                
        # Poll again after 1000ms
        self.root.after(1000, self.poll_messages)

    # =========================
    # USER LIST
    # =========================
    def build_user_list(self):
        ttk.Label(self.left_frame, text="Chats", font=("Arial", 12, "bold")).pack(pady=5)

        # Add new chat entry
        add_frame = ttk.Frame(self.left_frame)
        add_frame.pack(fill="x", padx=5, pady=5)

        self.new_user_entry = ttk.Entry(add_frame)
        self.new_user_entry.pack(side="left", fill="x", expand=True)

        ttk.Button(
            add_frame,
            text="Start Chat",
            command=self.start_new_chat
        ).pack(side="right", padx=5)

        # Chat buttons area
        self.user_buttons_frame = ttk.Frame(self.left_frame)
        self.user_buttons_frame.pack(fill="y", expand=True)
    
    def refresh_user_list(self):
        for w in self.user_buttons_frame.winfo_children():
            w.destroy()

        for uid in self.conversations.keys():
            ttk.Button(
                self.user_buttons_frame,
                text=f"User {uid}",
                command=lambda u=uid: self.load_conversation(u)
            ).pack(fill="x", padx=5, pady=2)

    def start_new_chat(self):
        if not self.connected:
            return
        
        recipient_id = self.new_user_entry.get().strip()

        if not recipient_id.isdigit() or not (0 < int(recipient_id) < 256):
            return

        recipient_id = int(recipient_id)

        if recipient_id == self.user.user_id:
            return  # Don't chat with yourself

        if recipient_id not in self.conversations:
            self.conversations[recipient_id] = []

        self.refresh_user_list()
        self.load_conversation(recipient_id)

        self.new_user_entry.delete(0, tk.END)
    
    # =========================
    # CHAT AREA
    # =========================
    def build_chat_area(self):
        self.sender_label = ttk.Label(
            self.right_frame,
            text=f"Sender: {self.recipient_id}",
            font=("Arial", 12, "bold")
        )
        self.sender_label.pack(fill="x", padx=5, pady=5)

        self.chat_display = tk.Text(self.right_frame, state="disabled", wrap="word")
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)
        self.chat_display.tag_configure("error", foreground="red")

        bottom = ttk.Frame(self.right_frame)
        bottom.pack(fill="x", padx=5, pady=5)

        self.message_entry = ttk.Entry(bottom)
        self.message_entry.pack(side="left", fill="x", expand=True)
        self.message_entry.bind("<Return>", self.send_message)

        ttk.Button(bottom, text="Send", command=self.send_message).pack(side="right")

    # =========================
    # SEND MESSAGE
    # =========================
    def send_message(self):
        if not self.connected or not self.recipient_id:
            return

        msg = self.message_entry.get().strip()
        if not msg:
            return
        
        sendStatus = self.user.send(self.recipient_id, msg) 
        self.add_message(self.recipient_id, "You", msg, sendStatus)
        
        self.message_entry.delete(0, tk.END)

    # =========================
    # MESSAGE MANAGEMENT
    # =========================
    def add_message(self, user_id, sender, message, tag=None):
        if user_id not in self.conversations:
            self.conversations[user_id] = []
            self.refresh_user_list()

        self.conversations[user_id].append((sender, message))

        if self.recipient_id == user_id:
            self.chat_display.config(state="normal")

            # Main message
            if tag == Status.PUSH_SUCCESS:
                self.chat_display.insert(
                    tk.END,
                    f"{sender}: {message}\n"
                )

            # Extra explanation line for errors
            if tag == Status.BUFFER_FULL:
                self.chat_display.insert(
                    tk.END,
                    f"Recipient's buffer is full\n",
                    "error"
                )
            elif tag == Status.INVALID_LENGTH:
                self.chat_display.insert(
                    tk.END,
                    f"Message exceeds 254 character limit\n",
                    "error"
                )
            elif tag == Status.ASSOCIATE_FAIL:
                self.chat_display.insert(
                    tk.END,
                    f"User association failed, attempting to reassociate\n",
                    "error"
                )
                self.connected = False
                self.status.config(text="Disconnected", foreground="red")
                self.id_entry.config(state="normal")
                self.set_ui_enabled(False)
                self.root.after(1000, self.reconnect)

            self.chat_display.config(state="disabled")
            self.chat_display.see(tk.END)


    def load_conversation(self, recipient_id):
        self.recipient_id = recipient_id
        self.chat_display.config(state="normal")
        self.chat_display.delete(1.0, tk.END)
        self.sender_label.config(text=f"Chatting with: User {recipient_id}")


        for sender, msg in self.conversations[recipient_id]:
            self.chat_display.insert(tk.END, f"{sender}: {msg}\n")

        self.chat_display.config(state="disabled")
    
    def reconnect(self):
        if self.connected:
            return  # Already reconnected somehow

        self.status.config(text="Reconnecting...", foreground="orange")
        self.user.associate()

        if self.user.associated:
            self.connected = True
            self.status.config(text=f"Connected as {self.user.user_id}", foreground="green")
            self.id_entry.config(state="disabled")
            self.set_ui_enabled(True)   # ← add this
            self.poll_messages()
        else:
            # Retry again in 5 seconds
            self.status.config(text="Reconnect failed, retrying...", foreground="red")
            self.root.after(5000, self.reconnect)


if __name__ == "__main__":
    root = tk.Tk()
    app = MessengerApp(root)
    root.mainloop()