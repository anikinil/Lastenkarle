import React, { useRef, useState } from "react";
import "./TextField.css";

// displays a one-line textfield with information,
// which can either be changed/entered (editable=true) or just viewed (editable=false)
const TextField = ({ title, placeholder, value, handleChange, editable, singleLine }) => {
    const textAreaRef = useRef(null);

    const [text, setText] = useState(value);

    const handleInput = (event) => {
        if (!singleLine) {
            const textarea = event.target;
            textarea.style.height = "auto"; // resets height
            textarea.style.height = `${textarea.scrollHeight}px`; // expands to fit content
        }
    };

    const handleKeyDown = (event) => {
        if (singleLine && event.key === "Enter") {
            event.preventDefault(); // prevents new lines
        }
    };

    return (
        <textarea
            ref={textAreaRef}
            title={title}
            className="text-field"
            value={text}
            onChange={(e) => {
                setText(e.target.value);
                handleChange(e.target.value);
                handleInput(e);
            }}
            onKeyDown={handleKeyDown}
            onInput={handleInput}
            placeholder={placeholder}
            disabled={!editable}
            style={{
                overflowX: singleLine ? "auto" : "hidden", // enables horizontal scrolling if singleLine=ture
                whiteSpace: singleLine ? "nowrap" : "normal", // prevents text from wrapping
                resize: singleLine ? "none" : "none", // disables manual resizing
            }}
        />
    );
};

export default TextField;
