import React, { useState } from "react";

const ChatBox = ({ onSend }) => {
  const [user, setUser] = useState("dev");
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    onSend(user, message);
    setMessage("");
  };

  return (
    <div className="bg-lightbg p-4 rounded-2xl shadow-md border border-gray-700">
      <h2 className="text-xl font-semibold mb-2 text-primary">Group Chat 💬</h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <input
          type="text"
          placeholder="Your name"
          value={user}
          onChange={(e) => setUser(e.target.value)}
          className="p-2 rounded bg-darkbg border border-gray-600 focus:outline-none"
        />
        <textarea
          placeholder="Say something like: I love beaches but not crowded cities..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="p-2 rounded bg-darkbg border border-gray-600 focus:outline-none h-24"
        />
        <button
          type="submit"
          className="bg-primary py-2 px-4 rounded hover:bg-[#0096c7] transition-all"
        >
          Send to AI
        </button>
      </form>
    </div>
  );
};

export default ChatBox;
