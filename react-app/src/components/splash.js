import "../App.css";

function Splash({ scrollToReport }) {
  // handleClick function to navigate to report section
  const handleClick = () => {
    scrollToReport();
  };

  return (
    <div className="splash-wrapper">
      <h1 className="slogan">
        Your <a className="slogan-eyecatcher">AI-Powered</a> Market Detective
      </h1>
      <div className="slogan-description">
        Enter your list of competitors to generate a brief report on their
        products, strategies and market perception
      </div>
      <div className="splash-buttons">
        <div
          href="#report"
          onClick={handleClick}
          className="call-to-action cta-v2"
        >
          Get stared
        </div>
        <a
          href="https://kellyshao.com/"
          target="_blank"
          className="my-profile-link"
          rel="noreferrer"
        >
          View Kelly &gt;
        </a>
      </div>
    </div>
  );
}
export default Splash;
