import React, { useState, useRef, useEffect } from "react";
import {
  Container,
  Row,
  Col,
  Form,
  Button,
  InputGroup,
  Alert,
  Spinner,
  Badge,
} from "react-bootstrap";
import Message from "./components/Message";
import ChartComponent from "./components/ChartComponent";
import DataTable from "./components/DataTable";
import { uploadFile, processQuery } from "./services/api";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add welcome message
    const welcomeMessage = {
      text:
        "👋 Welcome to Real Estate Analysis Chatbot! I can help you analyze property data and trends.\n\n" +
        "📁 First, upload your Excel file with real estate data, or I'll use the default dataset.\n\n" +
        "💡 Try queries like:\n" +
        "• 'Analyze Wakad'\n" +
        "• 'Compare Ambegaon Budruk and Aundh demand trends'\n" +
        "• 'Show price growth for Akurdi'",
      isUser: false,
    };
    setMessages([welcomeMessage]);
  }, []);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await uploadFile(file);
      setUploadedFile({
        name: file.name,
        path: response.file_path,
      });

      const botMessage = {
        text:
          `✅ File "${file.name}" uploaded successfully!\n\n` +
          `Found ${
            response.available_areas.length
          } areas: ${response.available_areas.slice(0, 5).join(", ")}${
            response.available_areas.length > 5 ? "..." : ""
          }\n\n` +
          `You can now ask me questions about these localities.`,
        isUser: false,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setError(
        err.response?.data?.error || "Failed to upload file. Please try again."
      );
    } finally {
      setIsLoading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      text: inputValue,
      isUser: true,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);
    setError(null);

    try {
      const response = await processQuery(inputValue, uploadedFile?.path);

      // Create bot response
      const botResponse = {
        text: response.summary,
        isUser: false,
      };

      const messagesWithResponse = [botResponse];

      // Add chart if available
      if (
        response.chart_data &&
        response.chart_data.labels &&
        response.chart_data.labels.length > 0
      ) {
        const chartMessage = {
          component: (
            <ChartComponent
              data={response.chart_data}
              type={response.chart_type || "line"}
            />
          ),
          isUser: false,
        };
        messagesWithResponse.push(chartMessage);
      }

      // Add table if available
      if (response.table_data && response.table_data.length > 0) {
        const tableMessage = {
          component: <DataTable data={response.table_data} />,
          isUser: false,
        };
        messagesWithResponse.push(tableMessage);
      }

      setMessages((prev) => [...prev, ...messagesWithResponse]);
    } catch (err) {
      const errorMessage = {
        text: `❌ Error: ${
          err.response?.data?.error ||
          "Failed to process query. Please try again."
        }`,
        isUser: false,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExampleQuery = (query) => {
    setInputValue(query);
  };

  const clearChat = () => {
    setMessages([
      {
        text: "Chat cleared. How can I help you with real estate analysis?",
        isUser: false,
      },
    ]);
  };

  return (
    <div className="App">
      <header className="app-header">
        <Container>
          <Row className="align-items-center">
            <Col>
              <h1 className="app-title">
                <span className="logo-icon">🏠</span>
                Real Estate Analysis Chatbot
              </h1>
              <p className="app-subtitle">
                Analyze property trends with AI-powered insights
              </p>
            </Col>
          </Row>
        </Container>
      </header>

      <Container fluid className="main-container">
        <Row className="h-100">
          <Col lg={3} md={4} className="sidebar">
            <div className="sidebar-content">
              <div className="upload-section">
                <h5 className="sidebar-title">📤 Upload Data</h5>
                <Form.Group>
                  <Form.Control
                    type="file"
                    accept=".xlsx,.xls"
                    onChange={handleFileUpload}
                    disabled={isLoading}
                    ref={fileInputRef}
                    className="file-input"
                  />
                </Form.Group>
                {uploadedFile && (
                  <Badge bg="success" className="mt-2 w-100">
                    📊 {uploadedFile.name}
                  </Badge>
                )}
              </div>

              <div className="examples-section">
                <h5 className="sidebar-title">💡 Example Queries</h5>
                <div className="d-grid gap-2">
                  <Button
                    variant="outline-secondary"
                    size="sm"
                    onClick={() => handleExampleQuery("Analyze Wakad")}
                    disabled={isLoading}
                    className="example-btn"
                  >
                    Analyze Wakad
                  </Button>
                  <Button
                    variant="outline-secondary"
                    size="sm"
                    onClick={() =>
                      handleExampleQuery(
                        "Compare Ambegaon Budruk and Aundh demand trends"
                      )
                    }
                    disabled={isLoading}
                    className="example-btn"
                  >
                    Compare Areas
                  </Button>
                  <Button
                    variant="outline-secondary"
                    size="sm"
                    onClick={() =>
                      handleExampleQuery("Show price growth for Akurdi")
                    }
                    disabled={isLoading}
                    className="example-btn"
                  >
                    Price Growth
                  </Button>
                </div>
              </div>

              <div className="actions-section">
                <Button
                  variant="outline-danger"
                  size="sm"
                  onClick={clearChat}
                  disabled={isLoading}
                  className="w-100"
                >
                  🗑️ Clear Chat
                </Button>
              </div>
            </div>
          </Col>

          <Col lg={9} md={8} className="chat-area">
            {error && (
              <Alert
                variant="danger"
                dismissible
                onClose={() => setError(null)}
              >
                {error}
              </Alert>
            )}

            <div className="messages-container">
              {messages.map((message, index) => (
                <Message
                  key={index}
                  message={message}
                  isUser={message.isUser}
                />
              ))}
              {isLoading && (
                <div className="loading-indicator">
                  <Spinner
                    animation="grow"
                    size="sm"
                    variant="primary"
                    className="me-2"
                  />
                  <Spinner
                    animation="grow"
                    size="sm"
                    variant="primary"
                    className="me-2"
                  />
                  <Spinner animation="grow" size="sm" variant="primary" />
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            <div className="input-section">
              <Form onSubmit={handleSubmit}>
                <InputGroup size="lg">
                  <Form.Control
                    type="text"
                    placeholder="Ask about real estate trends... (e.g., 'Analyze Wakad')"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    disabled={isLoading}
                    className="chat-input"
                  />
                  <Button
                    variant="primary"
                    type="submit"
                    disabled={!inputValue.trim() || isLoading}
                    className="send-button"
                  >
                    {isLoading ? (
                      <Spinner animation="border" size="sm" />
                    ) : (
                      <span style={{ fontSize: "1.2rem" }}>➤</span>
                    )}
                  </Button>
                </InputGroup>
              </Form>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
