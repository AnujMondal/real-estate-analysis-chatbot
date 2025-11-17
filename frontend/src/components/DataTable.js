import React from "react";
import { Table, Card, Button } from "react-bootstrap";
import "./DataTable.css";

const DataTable = ({ data, onDownload }) => {
  if (!data || data.length === 0) {
    return (
      <Card className="table-card">
        <Card.Body>
          <p className="text-muted">No data available</p>
        </Card.Body>
      </Card>
    );
  }

  // Get column headers from first row
  const columns = Object.keys(data[0]);

  const handleDownload = () => {
    if (onDownload) {
      onDownload();
      return;
    }

    // Convert to CSV
    const headers = columns.join(",");
    const rows = data.map((row) =>
      columns
        .map((col) => {
          const value = row[col];
          // Escape values that contain commas or quotes
          if (
            typeof value === "string" &&
            (value.includes(",") || value.includes('"'))
          ) {
            return `"${value.replace(/"/g, '""')}"`;
          }
          return value;
        })
        .join(",")
    );

    const csv = [headers, ...rows].join("\n");

    // Create download link
    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `real_estate_data_${Date.now()}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <Card className="table-card">
      <Card.Header className="d-flex justify-content-between align-items-center">
        <span className="fw-bold">Data Preview ({data.length} records)</span>
        <Button
          variant="outline-primary"
          size="sm"
          onClick={handleDownload}
          className="download-btn"
        >
          <i className="bi bi-download me-1"></i>
          Download CSV
        </Button>
      </Card.Header>
      <Card.Body className="p-0">
        <div className="table-responsive">
          <Table striped hover className="mb-0">
            <thead className="table-light sticky-header">
              <tr>
                {columns.map((col, index) => (
                  <th key={index}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {columns.map((col, colIndex) => (
                    <td key={colIndex}>
                      {typeof row[col] === "number"
                        ? row[col].toLocaleString()
                        : row[col]?.toString() || "-"}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      </Card.Body>
    </Card>
  );
};

export default DataTable;
