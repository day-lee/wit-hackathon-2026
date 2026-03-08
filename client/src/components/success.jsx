const Success = ({profile}) => {
  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>Talk to you soon, {profile.name}!</h2>
      <p>Your medication reminders have been successfully set up.</p>
      <p>You will receive timely notifications to take your medications.</p>
    </div>
  );
};

export default Success;