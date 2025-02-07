interface FormField {
    type: 'text' | 'dropdown' | 'input' | 'textarea';
    name: string;
    value?: string;
    defaultValue?: string;
    options?: string[];
}

const parseJsonToForm = (json: Record<string, any>): FormField[] => {
    const fields: FormField[] = [];

    const traverse = (obj: Record<string, any>) => {
        Object.entries(obj).forEach(([key, value]) => {
            if (key.startsWith("ignore:")) return;

            const cleanName = key.replace(/^(drop:|input:|textarea:)/, "");

            if (typeof value === "string") {
                fields.push({ type: "text", name: cleanName, value });

            } else if (typeof value === "object" && !Array.isArray(value)) {
                traverse(value);

            } else if (key.startsWith("drop:") && Array.isArray(value)) {
                let defaultValue = "";
                let selectedValue = "";
                const options: string[] = [];

                value.forEach(option => {
                    if (typeof option === "string") {
                        if (option.startsWith("default:")) {
                            defaultValue = option.replace("default:", "");
                        } else if (option.startsWith("selected:")) {
                            selectedValue = option.replace("selected:", "");
                        } else if (option.startsWith("opt:")) {
                            options.push(option.replace("opt:", ""));
                        }
                    }
                });

                fields.push({
                    type: "dropdown",
                    name: cleanName,
                    options,
                    defaultValue: selectedValue || defaultValue,
                });
            } else if (key.startsWith("input:")) {
                fields.push({
                    type: "input",
                    name: cleanName,
                    defaultValue: typeof value === "string" ? value : ""
                });
            } else if (key.startsWith("textarea:")) {
                fields.push({
                    type: "textarea",
                    name: cleanName,
                    defaultValue: typeof value === "string" ? value : ""
                });
            }
        });
    };

    traverse(json);
    return fields;
};

export default parseJsonToForm;