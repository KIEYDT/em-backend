import React, { useEffect, useState } from "react";
import "./App.css";
import { signin } from "./api";
import { useNavigate } from 'react-router-dom';


function Signin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await signin(email, password);
      if (response) {
        alert("Signin successfully.");
        navigate("/home");
      }
      
    } catch (err) {
      setError("invalid credentials");
    }
  };

  // DEBUG
  const DEBUG_LOGIN = async (e) => {
    e.preventDefault();
    try {
      const response = await signin("admin@em.com", "creation2281");
      if (response) {
        navigate("/home");
      }
    } catch (err) {
      setError("DEBUG LOGIN FAILED");
    }
  }

  return (
    <div className="login-container">
      <div className="picture-section">
        <p>Picture</p>
      </div>
      <form className="login-form" onSubmit={ handleSubmit }>
        <span className="top-login-label">Login</span>
        <div className="input-group">
          <div className="input-field">
            <span className="icon">👤</span>
            <input type="email" value={ email } onChange={ (e) => setEmail(e.target.value) } placeholder="Username"  />
          </div>
          <div className="input-field">
            <span className="icon">🔒</span>
            <input type="password" value={ password } onChange={ (e) => setPassword(e.target.value) } placeholder="Password" />
            <span className="toggle-password">👁️</span>
          </div>
        </div>
        <div className="remember-me">
          <input type="checkbox" id="remember" />
          <label htmlFor="remember">Remember me</label>
        </div>
        <button className="login-button" type="submit">Login</button>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <div className="social-login">
          <p>Or You Sign in with</p>
          <div className="social-icons">
            <button className="social-button">G</button>
            <button className="social-button">F</button>
          </div>
        </div>
        <div className="register-section">
          <a href="/register">Register</a>
        </div>
      </form>
    </div>
  );
}

export default Signin;