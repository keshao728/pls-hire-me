import React, { useState, useEffect } from "react";
import axios from "axios";
import "../App.css";

const Report = React.forwardRef((props, ref) => {
  const [siteNames, setSiteNames] = useState("");
  const [taskID, setTaskID] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  // Capitalize the first letter of each word in a string for visual appearance
  const capitalizeWords = (string) => {
    return string
      .split(" ")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  const siteNameArray = siteNames?.split(",").map((name) => name.trim());
  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    try {
      // Send a POST request to start the processing and obtain task ID
      const response = await axios.post("/process", {
        site_names: siteNameArray,
      });
      setTaskID(response.data.task_id);
    } catch (error) {
      console.error("There was an error!", error);
    }
  };

  // Check task status periodically
  useEffect(() => {
    const checkStatus = async () => {
      if (taskID) {
        try {
          const response = await axios.get(`/status/${taskID}`);

          if (response.data.status === "Completed") {
            const mappedResults = siteNameArray.map((name, index) => ({
              name,
              result: response.data.results[index],
            }));
            setResults(mappedResults);
            setTaskID("");
            setLoading(false);
          }
        } catch (error) {
          console.error("There was an error!", error);
        }
      }
    };

    const interval = setInterval(checkStatus, 5000);
    return () => clearInterval(interval);
  }, [taskID]);

  return (
    <div className="report-wrapper" ref={ref}>
      <div className="form-container">
        <img
          className="form-img"
          alt="dog asset"
          src="https://static.wixstatic.com/media/b7ca96_8ca8ccf3bc8749bea3db2e04ba90e9f4~mv2.png/v1/crop/x_0,y_0,w_252,h_335/fill/w_109,h_145,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/CHIA-dark.png"
        />
        <div className="form-slogan">
          Uncover valuable information about your competitors!
        </div>

        <form className="form" onSubmit={handleSubmit}>
          <label className="form-description">
            Enter the names of your rivals, separated by commas
          </label>
          <div className="input-container">
            <input
              type="text"
              className="form-input"
              placeholder="Company names..."
              value={siteNames}
              onChange={(e) => setSiteNames(e.target.value)}
            />
            <button type="submit" value="Submit" className="form-submit-button" disabled={loading}>
              <i className="fa-solid fa-magnifying-glass"></i>
            </button>
          </div>
        </form>
      </div>
      {loading ? (
        <div className="result-container">
          <p>Sorry no kachings to make this app spin faster, please wait!</p>
          <div className="hire-me">
            In the meantime, feel free to check out my social links!
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
          <img
            alt="loading"
            src="https://media.giphy.com/media/vbeNMLuswd7RR25lah/giphy.gif"
          ></img>
        </div>
      ) : results ? (
        <div className="result-wrapper">
          {results.map(({ name, result }, index) => (
            <div className="result-container" key={index}>
              <h2 className="form-slogan">{capitalizeWords(name)}</h2>
              {Object.entries(result).map(([question, details], idx) => (
                <div className="result-items-group" key={idx}>
                  <h3>{question}</h3>
                  <div>
                    <div className="result-items-title">Answer:</div>
                    <div className="result-items-report">{details.answer}</div>
                  </div>
                  <div>
                    <div className="result-items-title">Sources:</div>
                    {details.sources
                      .split("\n")
                      .flatMap((sourceLine) => sourceLine.split(","))
                      .map((source, i) => (
                        <div className="result-items-report" key={i}>
                          <a
                            className="source-link"
                            href={source.trim()}
                            target="_blank"
                            rel="noreferrer"
                          >
                            {source.trim()}
                          </a>
                        </div>
                      ))}
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>
      ) : (
        null
      )}
    </div>
  );
});

export default Report;
