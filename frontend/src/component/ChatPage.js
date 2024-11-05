import React, { useState } from "react";
import axios from "axios";
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  Avatar,
  ConversationHeader,
  TypingIndicator,
  MessageSeparator,
} from "@chatscope/chat-ui-kit-react";
import styles from "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";

const ChatComponent = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const currentDate = new Date(Date.now()).toLocaleDateString(undefined, {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  const handleInputChange = (newMessage) => {
    setInputValue(newMessage);
  };

  const handleSendMessage = async () => {
    if (inputValue.trim() === "") return;

    const userMessage = {
      message: inputValue,
      sentTime: new Date().toLocaleTimeString(),
      sender: "You",
      avatar: "./User.png",
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputValue("");
    setIsTyping(true);

    try {
      const response = await axios.get("/search", {
        params: {
          message: inputValue,
        },
      });

      const botMessage = {
        message: response.data.message,
        sentTime: new Date().toLocaleTimeString(),
        sender: "Bot",
        avatar: "/Bot.png",
      };

      setTimeout(() => {
        setMessages((prevMessages) => [...prevMessages, botMessage]);
        setIsTyping(false);
      }, 1000);
    } catch (error) {
      console.error("Error fetching response from API:", error);
      setIsTyping(false);
    }
  };

  return (
    <div>
      <MainContainer>
        <ChatContainer
          style={{
            height: window.innerHeight * 0.9,
          }}
        >
          <ConversationHeader>
            <Avatar name="Bot" src="/Bot.png" />
            <ConversationHeader.Content
              info="Bot with Pre-Trained AI Model"
              userName="Bot"
            />
            <ConversationHeader.Actions></ConversationHeader.Actions>
          </ConversationHeader>
          <MessageList
            typingIndicator={
              isTyping ? <TypingIndicator content="Bot is typing..." /> : null
            }
          >
            <MessageSeparator content={currentDate} />
            {messages.map((msg, index) => (
              <Message
                key={index}
                model={{
                  direction: msg.sender === "You" ? "outgoing" : "incoming",
                  message: msg.message,
                  position: "single",
                  sender: msg.sender,
                  sentTime: msg.sentTime,
                }}
              >
                <Avatar src={msg.avatar} name={msg.sender} size="40" />
              </Message>
            ))}
          </MessageList>
          <MessageInput
            placeholder="Type message here"
            value={inputValue}
            onChange={handleInputChange}
            onSend={handleSendMessage}
          />
        </ChatContainer>
      </MainContainer>
    </div>
  );
};

export default ChatComponent;
