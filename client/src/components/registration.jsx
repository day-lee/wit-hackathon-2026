import React from "react";

const Registration = ({ profile, setProfile, onNext }) => (
  <div className="fade-in">
    <p style={{ textAlign: "center", color: "#666" }}>
      Register to manage medications
    </p>
    <input
      className="input-field"
      placeholder="First Name"
      onChange={(e) => setProfile({ ...profile, name: e.target.value })}
    />
    <input
      className="input-field"
      placeholder="Last Name"
      onChange={(e) => setProfile({ ...profile, surname: e.target.value })}
    />
    <input
      className="input-field"
      type="tel"
      placeholder="Phone Number"
      onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
    />
    <button className="btn-primary" onClick={onNext}>
      Verify Phone Number
    </button>
  </div>
);

export default Registration;
