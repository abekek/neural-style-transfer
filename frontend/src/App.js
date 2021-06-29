import Home from "./pages/Home";
import Helmet from "react-helmet";

function App() {
  return (
    <div className="App">
      <Helmet>
        <style>
          {
            "body, html{ background-color: #F5F5F5; max-width: 100%; overflow-x: hidden}"
          }
        </style>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
                        integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossOrigin="anonymous"/>
      </Helmet>
      <Home />

      <footer>
          <h3>Built using</h3>
          <a href="https://aws.amazon.com/">
            <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Amazon_Web_Services_Logo.svg/1200px-Amazon_Web_Services_Logo.svg.png' alt="AWS" className="logo"/>
          </a>

          <a href="https://pytorch.org/">
            <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/PyTorch_logo_black.svg/1200px-PyTorch_logo_black.svg.png' alt="PyTorch" className="logo"/>
          </a>

          <a href="https://reactjs.org/">
            <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/1280px-React-icon.svg.png' alt="React" className="logo"/>
          </a>
      </footer>

      <style jsx>{`
      h3 {
        text-align: center;
      }

      .logo {
        height: 2em;
        margin-left: 1.5rem;
      }

      footer {
        width: 100%;
        height: 100px;
        border-top: 1px solid #eaeaea;
        display: flex;
        justify-content: center;
        align-items: center;
      }

      footer img {
        margin-left: 0.5rem;
      }

      footer a {
        display: flex;
        justify-content: center;
        align-items: center;
      }
      `}</style>
    </div>
  );
}

export default App;