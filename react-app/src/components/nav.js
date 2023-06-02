import "../App.css";

function Navigation({ scrollToReport }) {
  // handleClick function to navigate to report section
  const handleClick = () => {
    scrollToReport();
  };
  return (
    <div class="nav-wrapper">
      <div>Market Scope</div>
      <div className="nav-links">
        <a
          href="https://drive.google.com/file/d/1DSWOOlOKlCWxvTxkzEIcZKYd9tXdfvqN/view?usp=sharing"
          className="dev-link"
          target="_blank"
          rel="noreferrer"
        >
          Resume
        </a>
        <a
          href="https://github.com/keshao728"
          className="dev-link"
          target="_blank"
          rel="noreferrer"
        >
          Github
        </a>
        <a
          href="https://www.linkedin.com/in/keyingshao/"
          className="dev-link"
          target="_blank"
          rel="noreferrer"
        >
          Linkedln
        </a>
        <a
          href="https://kellyshao.com/"
          className="dev-link"
          target="_blank"
          rel="noreferrer"
        >
          Porfolio
        </a>
      </div>
      <div href="#report" onClick={handleClick} className="call-to-action">
        Get started
      </div>
    </div>
  );
}

export default Navigation;
