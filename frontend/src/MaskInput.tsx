import React, { ReactNode } from "react"
import {
  withStreamlitConnection,
  StreamlitComponentBase,
  Streamlit,
} from "./streamlit"
import CanvasDraw from "react-canvas-draw";

  
// Give everything a nice Streamlit style.
// (We're not really using this.)
import "./streamlit.css"

// We need to get to the hidden `ctx` variable in CanvasDraw
// so we create this type to get at it in a typesafe way.
interface CanvasDrawWithContext extends CanvasDraw {
  ctx: {
    [key: string]: CanvasRenderingContext2D,
  }
}

// The custom compnent we created.
class MaskInput extends StreamlitComponentBase {
  public render = (): ReactNode => {
    const imgUrl = this.props.args["imgUrl"]

    return (
      <>
        <CanvasDraw
          onChange={this.onCanvasChange}
          imgSrc={imgUrl}
          canvasWidth={700}
          canvasHeight={667}
        />
      </>
    )
  }

    /** Sets the Streamlit component value and sends a consoleMsg. */
  private setComponentValue = (value: object, consoleMsg?: object): void => {
    // Removes circular refernces from the console obect.
    const getCircularReplacer = () => {
      const seen = new WeakSet();
      return (_key: string, value: any) => {
        if (typeof value === "object" && value !== null) {
          if (seen.has(value)) {
            return '[REPEAT VALUE]';
          }
          seen.add(value);
        }
        return value;
      };
    };
    
    const toJSON = (x?: object) => {
      if (x == null)
        return undefined;
      else
        return JSON.parse(JSON.stringify(x, getCircularReplacer()));
    }

    // Set the state properly.
    Streamlit.setComponentValue({
        'value': value,
        'consoleMsg': toJSON(consoleMsg),
    })
  }

  /** Called every time the canvas changes, and sends the mask
   * back to the Streamlit server. */
  private onCanvasChange = (canvasDraw: CanvasDraw): void => {
    const contexts = (canvasDraw as CanvasDrawWithContext).ctx;
    // const width = canvasDraw.props.canvasWidth as number;
    // const height = canvasDraw.props.canvasHeight as number;
    
    const componentValue = {
        'state': this.state,
        'canvas': contexts.drawing.canvas.toDataURL()
    };

    this.setComponentValue(componentValue)
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
export default withStreamlitConnection(MaskInput)
