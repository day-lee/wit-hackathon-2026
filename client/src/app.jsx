import React, { useState } from "react";

import Registration from "./components/registration.jsx";
import Verification from "./components/Verification.jsx";
import MedicationForm from "./components/medicationForm.jsx";
import Success from "./components/success.jsx";

const App = () => {
  const [step, setStep] = useState(0);
  const [profile, setProfile] = useState({ name: "", surname: "", phone: "" });
  const [otp, setOtp] = useState("");
  const [medicines, setMedicines] = useState([""]);
  const [reminder, setReminder] = useState({ type: "call", time: "09:00" });

  return (
    <div className="card">
      <h2 className="title">HelloMeds</h2>
      {step === 0 && <Registration profile={profile} setProfile={setProfile} onNext={() => setStep(1)} />}
      {step === 1 && <Verification phone={profile.phone} setOtp={setOtp} onNext={() => setStep(2)} onBack={() => setStep(0)} />}
      {step === 2 && <MedicationForm profile={profile} medicines={medicines} setMedicines={setMedicines} reminder={reminder} setReminder={setReminder} onNext={() => setStep(3)} />}
      {step === 3 && <Success profile={profile} />}
    </div>
  );
};

export default App;