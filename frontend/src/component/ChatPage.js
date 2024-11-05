import React, { useState } from "react";
import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
} from "@chatscope/chat-ui-kit-react";

const ChatComponent = () => {
  const [messages, setMessages] = useState([
    {
      message: "Hello my friend",
      sentTime: "just now",
      sender: "Joe",
    },
  ]);
  const [inputValue, setInputValue] = useState("");

  const handleSend = () => {
    if (inputValue.trim() === "") return; // Ignore empty messages
    const newMessage = {
      message: inputValue,
      sentTime: new Date().toLocaleTimeString(),
      sender: "You",
    };
    setMessages([...messages, newMessage]);
    setInputValue(""); // Clear input after sending
  };

  return (
    <div style={{ position: "relative", height: "500px" }}>
      <MainContainer>
        <ChatContainer>
          <MessageList>
            {messages.map((msg, index) => (
              <Message key={index} model={msg} />
            ))}
          </MessageList>
          <MessageInput
            placeholder="Type message here"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onSend={handleSend}
          />
        </ChatContainer>
      </MainContainer>
    </div>
  );
};

export default ChatComponent;
