import "../App.css";

function Footer() {
  return (
    <div className="footer-wrapper">
      <div className="left-footer">
        <div>
          Market Scope by <a className="slogan-eyecatcher">Kelly Shao</a>
        </div>
        <div className="hire-me">(one of the) best engineer you may hire </div>
      </div>
      <ul className="social-icons">
        <li>
          <a
            href="https://drive.google.com/file/d/1DSWOOlOKlCWxvTxkzEIcZKYd9tXdfvqN/view?usp=sharing"
            target="_blank"
            className="social-icons-link"
            rel="noreferrer"
          >
            <i class="fa-regular fa-file"></i>
          </a>
        </li>
        <li>
          <a
            href="https://github.com/keshao728"
            target="_blank"
            className="social-icons-link"
            rel="noreferrer"
          >
            <i class="fa-brands fa-github"></i>
          </a>
        </li>
        <li>
          <a
            href="https://www.linkedin.com/in/keyingshao/"
            target="_blank"
            className="social-icons-link"
            rel="noreferrer"
          >
            <i class="fa-brands fa-linkedin"></i>
          </a>
        </li>
        <li>
          <a
            href="https://kellyshao.com/"
            className="social-icons-link"
            target="_blank"
            rel="noreferrer"
          >
            <i class="fa-solid fa-user"></i>
          </a>
        </li>
      </ul>
    </div>
  );
}
export default Footer;
