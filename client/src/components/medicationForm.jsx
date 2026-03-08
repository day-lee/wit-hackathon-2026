import React from "react";

const MedicationForm = ({
  profile,
  medicines,
  setMedicines,
  reminder,
  setReminder,
  onNext,
}) => {
  const addMedicine = () => {
    if (
      medicines.length < 10 &&
      medicines[medicines.length - 1].trim() !== ""
    ) {
      setMedicines([...medicines, ""]);
    }
  };

  const updateMedicine = (index, value) => {
    const updated = [...medicines];
    updated[index] = value;
    setMedicines(updated);
  };

  return (
    <div>
      <span className="badge">
        Patient: {profile.name} {profile.surname}
      </span>

      <h4 style={{ margin: "10px 0", color: "#333" }}>
        My Medications (Max 10)
      </h4>

      {medicines.map((med, i) => (
        <div
          key={i}
          style={{ display: "flex", gap: "5px", marginBottom: "10px" }}
        >
          <input
            className="input-field"
            style={{ marginBottom: 0 }}
            placeholder={`Medicine ${i + 1}`}
            value={med}
            onChange={(e) => updateMedicine(i, e.target.value)}
          />
          {i === medicines.length - 1 && medicines.length < 10 && (
            <button type="button" className="btn-add" onClick={addMedicine}>
              +
            </button>
          )}
        </div>
      ))}

      <div className="info-box">
        <label
          style={{
            fontWeight: "bold",
            display: "block",
            marginBottom: "5px",
            fontSize: "14px",
          }}
        >
          Reminder Schedule
        </label>
        <input
          type="time"
          className="input-field"
          value={reminder.time}
          onChange={(e) => setReminder({ ...reminder, time: e.target.value })}
        />

        <div style={{ fontSize: "12px", color: "#555", lineHeight: "1.5" }}>
          <strong>Twilio Escalation Protocol:</strong>
          <br />• 5m before:{" "}
          <span style={{ color: "#1a73e8" }}>Reminder Call</span>
          <br />• 5m after: <span style={{ color: "#d93025" }}>Retry Call</span>
          <br />• 6m after:{" "}
          <span style={{ color: "#34a853" }}>SMS Confirmation</span>
        </div>
      </div>
      <input type="checkbox" id="consent" name="consent" value="consent" style={{ marginTop: "20px" }} />
      <label htmlFor="consent"> I am hereby consent to the terms and conditions </label>

      <button
        className="btn-primary"
        style={{ backgroundColor: "#34a853", marginTop: "20px" }}
        onClick={onNext}
      >
        Save & Activate
      </button>
    </div>
  );
};

export default MedicationForm;
