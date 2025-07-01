import React, { useEffect, useState } from "react";
import axios from "../axiosInstance";

const AdminDashboard = () => {
  const [templates, setTemplates] = useState([]);
  const [templateName, setTemplateName] = useState("");
  const [fields, setFields] = useState([{ name: "", type: "text", required: false }]);
  const [workflows, setWorkflows] = useState([]);
  const [workflowStates, setWorkflowStates] = useState("");
  const [transitions, setTransitions] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState("");

  useEffect(() => {
    fetchTemplates();
    fetchWorkflows();
  }, []);

  const fetchTemplates = async () => {
    const res = await axios.get("/form-templates/");
    setTemplates(res.data);
  };

  const fetchWorkflows = async () => {
    const res = await axios.get("/workflows/");
    setWorkflows(res.data);
  };

  const handleAddField = () => {
    setFields([...fields, { name: "", type: "text", required: false }]);
  };

  const handleFieldChange = (index, key, value) => {
    const newFields = [...fields];
    newFields[index][key] = value;
    setFields(newFields);
  };

  const createTemplate = async () => {
    const schema = { fields };
    const res = await axios.post("/form-template/", {
      name: templateName,
      schema,
    });
    alert("Form template created");
    fetchTemplates();
  };

  const createWorkflow = async () => {
    const statesArray = workflowStates.split(",").map((s) => s.trim());
    const res = await axios.post("/workflow-definition/", {
      form_template: selectedTemplate,
      states: statesArray,
      transitions,
    });
    alert("Workflow created");
  };

  const handleAddTransition = () => {
    setTransitions([
      ...transitions,
      { from_state: "", to_state: "", allowed_roles: [], logical_type: "OR" },
    ]);
  };

  const handleTransitionChange = (index, key, value) => {
    const newTrans = [...transitions];
    if (key === "allowed_roles") {
      newTrans[index][key] = value.split(",").map((r) => r.trim());
    } else {
      newTrans[index][key] = value;
    }
    setTransitions(newTrans);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Admin Dashboard</h2>

      <div className="mb-6">
        <h3 className="font-semibold">Create Form Template</h3>
        <input
          placeholder="Template Name"
          value={templateName}
          onChange={(e) => setTemplateName(e.target.value)}
          className="border p-2 block mb-2"
        />
        {fields.map((field, index) => (
          <div key={index} className="mb-2">
            <input
              placeholder="Field Name"
              value={field.name}
              onChange={(e) => handleFieldChange(index, "name", e.target.value)}
              className="border p-1 mr-2"
            />
            <select
              value={field.type}
              onChange={(e) => handleFieldChange(index, "type", e.target.value)}
              className="border p-1 mr-2"
            >
              <option value="text">Text</option>
              <option value="number">Number</option>
              <option value="date">Date</option>
            </select>
            <label>
              <input
                type="checkbox"
                checked={field.required}
                onChange={(e) => handleFieldChange(index, "required", e.target.checked)}
                className="mr-1"
              />
              Required
            </label>
          </div>
        ))}
        <button onClick={handleAddField} className="bg-gray-200 p-1 mr-2">+ Field</button>
        <button onClick={createTemplate} className="bg-blue-500 text-white p-1">Create Template</button>
      </div>

      {/* List of Existing Form Templates */}
      <div className="mb-8">
        <h3 className="font-semibold mb-2">Existing Form Templates</h3>
        <table className="min-w-full border text-sm mb-4">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-2 py-1">ID</th>
              <th className="border px-2 py-1">Name</th>
              <th className="border px-2 py-1">Created At</th>
            </tr>
          </thead>
          <tbody>
            {templates.map((tpl) => (
              <tr key={tpl.id}>
                <td className="border px-2 py-1">{tpl.id}</td>
                <td className="border px-2 py-1">{tpl.name}</td>
                <td className="border px-2 py-1">{tpl.created_at ? new Date(tpl.created_at).toLocaleString() : ''}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div>
        <h3 className="font-semibold">Create Workflow</h3>
        <select
          value={selectedTemplate}
          onChange={(e) => setSelectedTemplate(e.target.value)}
          className="border p-2 block mb-2"
        >
          <option value="">Select Template</option>
          {templates.map((tpl) => (
            <option key={tpl.id} value={tpl.id}>{tpl.name}</option>
          ))}
        </select>
        <input
          placeholder="Comma separated states"
          value={workflowStates}
          onChange={(e) => setWorkflowStates(e.target.value)}
          className="border p-2 block mb-2"
        />
        {transitions.map((trans, index) => (
          <div key={index} className="mb-2">
            <input
              placeholder="From State"
              value={trans.from_state}
              onChange={(e) => handleTransitionChange(index, "from_state", e.target.value)}
              className="border p-1 mr-2"
            />
            <input
              placeholder="To State"
              value={trans.to_state}
              onChange={(e) => handleTransitionChange(index, "to_state", e.target.value)}
              className="border p-1 mr-2"
            />
            <input
              placeholder="Comma separated roles"
              value={trans.allowed_roles.join(", ")}
              onChange={(e) => handleTransitionChange(index, "allowed_roles", e.target.value)}
              className="border p-1 mr-2"
            />
            <select
              value={trans.logical_type}
              onChange={(e) => handleTransitionChange(index, "logical_type", e.target.value)}
              className="border p-1"
            >
              <option value="OR">OR</option>
              <option value="AND">AND</option>
            </select>
          </div>
        ))}
        <button onClick={handleAddTransition} className="bg-gray-200 p-1 mr-2">+ Transition</button>
        <button onClick={createWorkflow} className="bg-green-500 text-white p-1">Create Workflow</button>
      </div>

      {/* List of Existing Workflows */}
      <div className="mt-8">
        <h3 className="font-semibold mb-2">Existing Workflows</h3>
        <table className="min-w-full border text-sm mb-4">
          <thead>
            <tr className="bg-gray-100">
              <th className="border px-2 py-1">ID</th>
              <th className="border px-2 py-1">Form Template ID</th>
              <th className="border px-2 py-1">States</th>
              <th className="border px-2 py-1">Transitions</th>
            </tr>
          </thead>
          <tbody>
            {workflows.map((wf) => (
              <tr key={wf.id}>
                <td className="border px-2 py-1">{wf.id}</td>
                <td className="border px-2 py-1">{wf.form_template}</td>
                <td className="border px-2 py-1">{Array.isArray(wf.states) ? wf.states.join(", ") : ''}</td>
                <td className="border px-2 py-1">
                  {Array.isArray(wf.transitions) && wf.transitions.length > 0 ? (
                    <ul className="list-disc pl-4">
                      {wf.transitions.map((t, idx) => (
                        <li key={t.id || idx}>
                          {t.from_state} → {t.to_state} [Roles: {t.allowed_roles.join(", ")}, {t.logical_type}]
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <span>No transitions</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminDashboard;
