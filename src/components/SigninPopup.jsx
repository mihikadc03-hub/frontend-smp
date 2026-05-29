import { useState } from "react";
import { useAuth } from "../context/AuthContext";

export default function SigninPopup() {
  const { isAuthOpen, setIsAuthOpen, login } = useAuth();
  const [isRegister, setIsRegister] = useState(false);
  const [inputValue, setInputValue] = useState("");

  if (!isAuthOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim()) {
      login(inputValue);
    }
  };

  return (
    <div className="modal-backdrop" onClick={() => setIsAuthOpen(false)}>
      <div className="modal auth-modal" onClick={(e) => e.stopPropagation()}>
        <div className="auth-header">
          <button 
            type="button"
            className={`auth-tab ${!isRegister ? "active" : ""}`} 
            onClick={() => setIsRegister(false)}
          >
            Login
          </button>
          <button 
            type="button"
            className={`auth-tab ${isRegister ? "active" : ""}`} 
            onClick={() => setIsRegister(true)}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-field">
            <label>Email or Username</label>
            <input 
              type="text" 
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              required 
            />
          </div>
          <div className="form-field">
            <label>Password</label>
            <input type="password" required />
          </div>

          <div className="modal-actions auth-actions mt-4">
            <button type="button" className="btn btn-ghost" onClick={() => setIsAuthOpen(false)}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {isRegister ? "Create Account" : "Sign In"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}