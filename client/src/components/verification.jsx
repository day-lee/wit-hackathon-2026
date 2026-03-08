import React from "react";

const Verification = ({ phone, setOtp, onNext, onBack }) => (
  <div style={{ textAlign: "center" }}>
    <p>
      We sent a 6-digit code to <br />
      <strong>{phone}</strong>
    </p>
    <input
      className="input-field"
      style={{ textAlign: "center", fontSize: "24px", letterSpacing: "8px" }}
      maxLength="6"
      placeholder="000000"
      onChange={(e) => setOtp(e.target.value)}
    />
    <button className="btn-primary" onClick={onNext}>
      Confirm & Enter Portal
    </button>
    <p
      style={{
        fontSize: "12px",
        color: "#888",
        marginTop: "10px",
        cursor: "pointer",
      }}
      onClick={onBack}
    >
      Change phone number
    </p>
  </div>
);

export default Verification;
