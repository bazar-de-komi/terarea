const parseJsonToForm = (json) => {
    const fields = [];

    const traverse = (obj) => {
        Object.entries(obj).forEach(([key, value]) => {
            if (key.startsWith("ignore:")) return;

            const cleanName = key.replace(/^(drop:|input:|textarea:)/, "");

            if (typeof value === "string") {
                fields.push({ type: "text", name: cleanName, value });
            
            } else if (typeof value === "object" && !Array.isArray(value)) {
                traverse(value);
            
            } else if (key.startsWith("drop:")) {
            
                let defaultValue = "";
                let selectedValue = "";
                const options = [];

                value.forEach(option => {
                    if (option.startsWith("default:")) {
                        defaultValue = option.replace("default:", "");
                    } else if (option.startsWith("selected:")) {
                        selectedValue = option.replace("selected:", "");
                    } else if (option.startsWith("opt:")) {
                        options.push(option.replace("opt:", ""));
                    }
                });

                fields.push({
                    type: "dropdown",
                    name: cleanName,
                    options,
                    defaultValue: selectedValue || defaultValue,
                });
            } else if (key.startsWith("input:")) {
                
                fields.push({ type: "input", name: cleanName, defaultValue: value || "" });
            } else if (key.startsWith("textarea:")) {
                
                fields.push({ type: "textarea", name: cleanName, defaultValue: value || "" });
            }
        });
    };

    traverse(json);
    return fields;
};

export default parseJsonToForm;
