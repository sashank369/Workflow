import React, { useEffect, useState } from "react";
import axios from "../axiosInstance";

const EmployeeDashboard = () => {
  const [templates, setTemplates] = useState([]);
  const [formData, setFormData] = useState({});
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [submissions, setSubmissions] = useState([]);

  useEffect(() => {
    fetchTemplates();
    fetchSubmissions();
  }, []);

  const fetchTemplates = async () => {
    const res = await axios.get("/form-templates/");
    setTemplates(res.data);
  };

  const fetchSubmissions = async () => {
    const res = await axios.get("/my-submissions/");
    setSubmissions(res.data);
  };

  const handleSelectTemplate = (template) => {
    setSelectedTemplate(template);
    setFormData({});
  };

  const handleChange = (name, value) => {
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async () => {
    try {
      const res = await axios.post("/submit-form/", {
        form_template: selectedTemplate.id,
        data: formData,
      });
      alert("Form submitted");
      setSelectedTemplate(null);
      fetchSubmissions();
    } catch (error) {
      alert(error.response?.data?.error || "Error submitting form");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Employee Dashboard</h2>

      <div className="mb-6">
        <h3 className="font-semibold mb-2">Available Form Templates</h3>
        {templates.map((tpl) => (
          <div key={tpl.id} className="mb-2">
            <button
              className="bg-blue-500 text-white px-3 py-1 rounded"
              onClick={() => handleSelectTemplate(tpl)}
            >
              Fill {tpl.name}
            </button>
          </div>
        ))}
      </div>

      {selectedTemplate && (
        <div className="mb-6 border p-4">
          <h3 className="font-semibold mb-2">Filling: {selectedTemplate.name}</h3>
          {selectedTemplate.schema.fields.map((field, index) => (
            <div key={index} className="mb-2">
              <label className="block font-medium mb-1">{field.name}:</label>
              <input
                type={field.type}
                className="border p-2 w-full"
                required={field.required}
                onChange={(e) => handleChange(field.name, e.target.value)}
              />
            </div>
          ))}
          <button
            className="bg-green-600 text-white px-3 py-1 rounded"
            onClick={handleSubmit}
          >
            Submit Form
          </button>
        </div>
      )}

      <div>
        <h3 className="font-semibold mb-2">My Submissions</h3>
        {submissions.map((sub, index) => (
          <div key={index} className="border p-2 mb-2">
            <div className="font-bold">{sub.submission.form_template_details.name}</div>
            <div>Submitted At: {new Date(sub.submission.submitted_at).toLocaleString()}</div>
            <div>Current State: {sub.current_state}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EmployeeDashboard;
