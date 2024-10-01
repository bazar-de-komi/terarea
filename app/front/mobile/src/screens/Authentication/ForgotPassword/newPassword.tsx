import React, {useState} from "react";
import { View, Text, Image, StyleSheet, ScrollView} from "react-native";
import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from "../../../components/CustomerButton";
import { useNavigation } from "@react-navigation/native";

const NewPassword = () => {
    const [code, setCode] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const Navigation = useNavigation();
    
    const SignSubmitPressed = () => {
        console.warn("Submit");
    }

    const loginPressed = () => {
        console.warn("Log in");
        Navigation.navigate("Sign In");
    }

    return (
    <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.NewPasswordContainer}>
            <Text style={styles.NewPasswordTitle}>Add New password</Text>
            <CustomerInput
            placeholder="code"
            value={code}
            setValue={setCode}
            secureTextEntry={false}
            />
            <CustomerInput
            placeholder="Enter your new password"
            value={newPassword}
            setValue={setNewPassword}
            secureTextEntry={false}
            />
            <CustomerButton text="Submit" onPress={SignSubmitPressed} bgColor={""} fgColor={""}/>

            <CustomerButton
            text="Back to Sign in"
            onPress={loginPressed}
            type="TERTIARY"
            bgColor={""}
            fgColor={""}
            />

        </View>
    </ScrollView>
    );
};

const styles = StyleSheet.create({
    NewPasswordContainer: {
        alignItems: 'center',
        padding: 20,
    },
    IftttLogo: {
        width: '40%',
        maxWidth: 300,
        maxHeight: 200,
    },
    logoButtonContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        width: '80%',
        // backgroundColor: '#FAE9EA',
        borderRadius: 5,
        padding: 10,
        marginVertical: 5,
    },
    logo: {
        right: 80,
        top: 40,
        width: 24,
        height: 24,
        marginRight: 10,
    },
    NewPasswordTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#051C60',
        margin: 10,
    },
})

export default NewPassword;