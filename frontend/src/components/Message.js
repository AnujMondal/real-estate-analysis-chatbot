import React from "react";
import { Card } from "react-bootstrap";
import "./Message.css";

const Message = ({ message, isUser }) => {
  return (
    <div
      className={`message-wrapper ${isUser ? "user-message" : "bot-message"}`}
    >
      <Card className={`message-card ${isUser ? "user-card" : "bot-card"}`}>
        <Card.Body>
          {!isUser && (
            <div className="bot-icon">
              <i className="bi bi-robot"></i>
            </div>
          )}
          <div className="message-content">
            {message.text && <p className="message-text">{message.text}</p>}
            {message.component}
          </div>
        </Card.Body>
      </Card>
    </div>
  );
};

export default Message;
