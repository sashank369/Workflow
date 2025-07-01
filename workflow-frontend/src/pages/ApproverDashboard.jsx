import React, { useEffect, useState } from "react";
import axios from "../axiosInstance";

const ApproverDashboard = () => {
  const [pendingSubmissions, setPendingSubmissions] = useState([]);
  const [selectedSubmission, setSelectedSubmission] = useState(null);
  const [nextState, setNextState] = useState("");
  const [availableTransitions, setAvailableTransitions] = useState([]);

  useEffect(() => {
    fetchPending();
  }, []);

  const fetchPending = async () => {
    const res = await axios.get("/pending-approvals/");
    setPendingSubmissions(res.data);
  };

  const selectSubmission = async (submission) => {
    setSelectedSubmission(submission);
    const res = await axios.get(`/transitions/${submission.submission.id}/`);
    setAvailableTransitions(res.data);
  };

  const handleTransition = async () => {
    if (!nextState) return alert("Please select next state");
    try {
      const res = await axios.post("/transition/", {
        submission_id: selectedSubmission.submission.id,
        next_state: nextState,
      });
      alert("Transitioned successfully");
      setSelectedSubmission(null);
      setNextState("");
      fetchPending();
    } catch (error) {
      alert(error.response?.data?.error || "Error transitioning workflow");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Approver Dashboard</h2>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <h3 className="font-semibold mb-2">Pending Submissions</h3>
          {pendingSubmissions.map((sub) => (
            <div key={sub.id} className="border p-2 mb-2">
              <div className="font-bold">{sub.submission.form_template_details.name}</div>
              <div>Submitted by: {sub.submission.submitted_by}</div>
              <div>Current State: {sub.current_state}</div>
              <button
                className="mt-2 bg-blue-500 text-white px-2 py-1 rounded"
                onClick={() => selectSubmission(sub)}
              >
                View & Transition
              </button>
            </div>
          ))}
        </div>

        {selectedSubmission && (
          <div className="border p-4">
            <h3 className="font-semibold mb-2">Submission Details</h3>
            <pre className="text-sm bg-gray-100 p-2 mb-2">
              {JSON.stringify(selectedSubmission.data, null, 2)}
            </pre>
            <label className="block mb-2">Select Next State:</label>
            <select
              value={nextState}
              onChange={(e) => setNextState(e.target.value)}
              className="border p-2 mb-4 w-full"
            >
              <option value="">-- Select --</option>
              {availableTransitions.map((t, i) => (
                <option key={i} value={t.to_state}>
                  {t.to_state}
                </option>
              ))}
            </select>
            <button
              className="bg-green-600 text-white px-3 py-1 rounded"
              onClick={handleTransition}
            >
              Transition
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ApproverDashboard;
