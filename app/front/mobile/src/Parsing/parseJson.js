export const parseJsonToForm = (json) => {
    const fields = [];

    const traverse = (obj, currentPath) => {
        Object.entries(obj).forEach(([key, value]) => {
            if (key.startsWith("ignore:")) return;

            const cleanName = key.replace(/^(drop:|input:|textarea:)/, "");
            const newPath = currentPath ? `${currentPath}.${cleanName}` : cleanName;

            const newNameFormat = (name, path) => {
                if (path.includes("verification")) {
                    const parts = path.split(".");
                    const index = parts.indexOf("verification");
                    if (index !== -1 && index + 1 < parts.length) {
                        return parts[index + 1];
                    }
                }
                return name;
            };

            const newName = newNameFormat(cleanName, newPath);

            if (typeof value === "object" && !Array.isArray(value)) {
                traverse(value, newPath);
            } else if (key.startsWith("drop:") && Array.isArray(value)) {
                let defaultValue = "";
                let selectedValue = "";
                const options = [];

                value.forEach(option => {
                    if (typeof option === "string") {
                        if (option.startsWith("default:")) {
                            defaultValue = option.replace("default:", "");
                            options.push(option.replace("default:", ""));
                        } else if (option.startsWith("selected:")) {
                            selectedValue = option.replace("selected:", "");
                            options.push(option.replace("selected:", ""));
                        } else if (option.startsWith("opt:")) {
                            options.push(option.replace("opt:", ""));
                        }
                    }
                });

                fields.push({
                    type: "dropdown",
                    name: newName,
                    path: newPath,
                    options,
                    defaultValue: selectedValue || defaultValue,
                });

            } else if (key.startsWith("input:")) {
                fields.push({
                    type: "input",
                    name: cleanName,
                    path: newPath,
                    defaultValue: typeof value === "string" ? value : "",
                    placeholder: typeof value === "string" ? value : ""
                });
            } else if (key.startsWith("textarea:")) {
                fields.push({
                    type: "textarea",
                    name: cleanName,
                    path: newPath,
                    defaultValue: typeof value === "string" ? value : "",
                    placeholder: typeof value === "string" ? value : ""
                });
            }
        });
    };

    traverse(json, "");
    return fields;
};

export const injectFormValuesIntoJson = (json, fields) => {
    const updatedJson = { ...json };

    fields.forEach((field) => {
        const pathParts = field.path.split(".");
        let current = updatedJson;

        for (let i = 0; i < pathParts.length - 1; i++) {
            if (!current[pathParts[i]]) {
                current[pathParts[i]] = {};
            }
            current = current[pathParts[i]];
        }

        const finalKey = pathParts[pathParts.length - 1];
        const originalKey = Object.keys(current).find(k => k.endsWith(finalKey));

        if (!originalKey) return;

        if (field.type === "dropdown") {
            const newOptions = current[originalKey].map((option) => {
                if (option.startsWith("default:") && option.replace("default:", "") === field.defaultValue) {
                    return option;
                } else if (option.startsWith("opt:") && option.replace("opt:", "") === field.defaultValue) {
                    return `selected:${field.defaultValue}`;
                }
                return option;
            });

            current[originalKey] = newOptions;
        } else {
            if (field.value) {
                current[originalKey] = field.value;
            } else {
                current[originalKey] = field.defaultValue;
            }
        }
    });

    return updatedJson;
};
