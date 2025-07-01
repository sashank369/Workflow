import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import jwtDecode from "jwt-decode";

const LoginPage = () => {
  const [usernam, setUsername] = useState("");
  const [passwor, setPassword] = useState("");
  const navigate = useNavigate();
  const handleLogin = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8080/realms/demo-realm/protocol/openid-connect/token",
        new URLSearchParams({
          grant_type: "password",
          client_id: "django-backend",
          username:usernam,
          password:passwor,
        }),
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      const token = response.data.access_token;
      localStorage.setItem("token", token);
      const decoded = jwtDecode(token);
      const roles = decoded.realm_access.roles;
      console.log(roles);
      if (roles.includes("Admin")) navigate("/admin");
      else if (roles.includes("Employee")) navigate("/employee");
      else if (roles.includes("HR") || roles.includes("Manager"))
        navigate("/approver");
      else alert("No dashboard available for your role.");
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h2 className="text-2xl mb-4 font-bold">Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={usernam}
        onChange={(e) => setUsername(e.target.value)}
        className="block w-full p-2 border mb-3"
      />
      <input
        type="password"
        placeholder="Password"
        value={passwor}
        onChange={(e) => setPassword(e.target.value)}
        className="block w-full p-2 border mb-3"
      />
      <button onClick={handleLogin} className="bg-blue-500 text-white px-4 py-2">
        Login
      </button>
    </div>
  );
};

export default LoginPage;
