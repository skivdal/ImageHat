import { useState } from "react";
import "./App.css"
import Cameras from "./components/Cameras.tsx";
import Images from "./components/Images.tsx";

const App = () => {
  const [selectedView, setSelectedView] = useState<string>("camera");
  return (<>
        <div className={"header"}>
          <h3>Metadata order visualization</h3>
          <div className={"header-group"}>
            <h5 className={"header-button"} onClick={() => setSelectedView("image")}>By image</h5>
            <h5 className={"header-button"} onClick={() => setSelectedView("camera")}>By camera</h5>
          </div>
        </div>
        {selectedView == "camera" && (
            <Cameras></Cameras>
        )}
        {selectedView == "image" && (
            <Images></Images>
        )}
      </>
  );
};

export default App;

