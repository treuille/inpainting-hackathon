import React, { ReactNode } from "react"
import {
  withStreamlitConnection,
  StreamlitComponentBase,
  Streamlit,
} from "./streamlit"
import CanvasDraw from "react-canvas-draw";

// We import bootstrap.css and streamlit.css to get some simple default
// styling for our text and button. You can remove or replace these!
import "bootstrap/dist/css/bootstrap.min.css"
import "./streamlit.css"

interface State {
  numClicks: number
}

/**
 * This is a React-based component template. It's an alternative to the
 * event-based component pattern. Rather than handling RENDER_EVENT events,
 * you write your rendering logic in the render() function, which is
 * called automatically when appropriate.
 */
class MaskInput extends StreamlitComponentBase<State> {
  public state = { numClicks: 0 }

  /** A reference to the canvas object so we can get its data. */
  canvasDraw?: CanvasDraw; 
  
  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const name = this.props.args["name"]

    // When the button is clicked, we'll increment our "numClicks" state

    // variable, and send its new value back to Streamlit, where it'll
    // be available to the Python program.
    // https://github.com/embiem/react-canvas-draw/blob/master/demo/src/index.
    return (
      <>
        <div>Hello, {name}!!!</div>
        <button onClick={this.onClicked} disabled={this.props.disabled}>
          Click Me!
        </button>
        <CanvasDraw
          ref={(canvasDraw: CanvasDraw) => (this.canvasDraw = canvasDraw)}
          onChange={this.onCanvasChange} />
      </>
    )
  }

    /** Sets the Streamlit component value and sends a consoleMsg. */
  private setComponentValue = (value: object, consoleMsg: object): void => {
    // Removes circular refernces from the console obect.
    const getCircularReplacer = () => {
      const seen = new WeakSet();
      return (_key: string, value: any) => {
        if (typeof value === "object" && value !== null) {
          if (seen.has(value)) {
            return;
          }
          seen.add(value);
        }
        return value;
      };
    };
    
    const toJSON = (x: object) => {
      return  JSON.parse(JSON.stringify(x, getCircularReplacer()));
    }

    // Set the state properly.
    Streamlit.setComponentValue({
        'value': value,
        'consoleMsg': toJSON(consoleMsg),
    })
  }

  /** Click handler for our "Click Me!" button. */
  private onCanvasChange = (..._args : any[]): void => {
    // Set the state properly.
    this.setState(
      prevState => ({ numClicks: prevState.numClicks + 200 }),
      () => this.setComponentValue(this.state, {
        'lines': this.canvasDraw?.getSaveData(),
        'canvasDraw': (this.canvasDraw as any).canvas,
        //'canvasDraw': (this.canvasDraw as any).canvas.context.getImageData(10, 10, 50, 50),
      })
    )
  }

  /** Click handler for our "Click Me!" button. */
  private onClicked = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    this.setState(
      prevState => ({ numClicks: prevState.numClicks + 1 }),
      () => Streamlit.setComponentValue({
          'num_clicks': this.state.numClicks,
          'console': 'this.onClicked'
      })
    )
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(MaskInput)
