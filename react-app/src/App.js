import React, { useRef } from "react";
import Splash from "./components/splash.js";
import Report from "./components/report.js";
import Nav from "./components/nav.js";
import Footer from "./components/footer.js";
import "./App.css";

function App() {
  const reportRef = useRef(null);

  const scrollToReport = () => {
    if (reportRef.current) {
      window.scrollTo({
        top: reportRef.current.offsetTop,
        behavior: "smooth",
      });
    }
  };
  return (
    <div className="app-wrapper">
      <Nav scrollToReport={scrollToReport} />
      <Splash scrollToReport={scrollToReport} />
      <Report ref={reportRef} />
      <Footer />
    </div>
  );
}

export default App;
