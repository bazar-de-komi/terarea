interface FormField {
    type: 'text' | 'dropdown' | 'input' | 'textarea';
    name: string;
    path: string;
    value?: string;
    defaultValue?: string;
    options?: string[];
}

const parseJsonToForm = (json: Record<string, any>): FormField[] => {
    const fields: FormField[] = [];

    const traverse = (obj: Record<string, any>, currentPath: string) => {
        Object.entries(obj).forEach(([key, value]) => {
            if (key.startsWith("ignore:")) return;

            const cleanName = key.replace(/^(drop:|input:|textarea:)/, "");
            const newPath = currentPath ? `${currentPath}.${cleanName}` : cleanName;

            const newNameFormat = (name: string, path: string) => {
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

            if (typeof value === "string") {
                return;
                // fields.push({ type: "text", name: cleanName, value, path: newPath });

            } else if (typeof value === "object" && !Array.isArray(value)) {
                traverse(value, newPath);

            } else if (key.startsWith("drop:") && Array.isArray(value)) {
                let defaultValue = "";
                let selectedValue = "";
                const options: string[] = [];

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
                    defaultValue: typeof value === "string" ? value : ""
                });
            } else if (key.startsWith("textarea:")) {
                fields.push({
                    type: "textarea",
                    name: cleanName,
                    path: newPath,
                    defaultValue: typeof value === "string" ? value : ""
                });
            }
        });
    };

    traverse(json, "");
    return fields;
};

export default parseJsonToForm;
