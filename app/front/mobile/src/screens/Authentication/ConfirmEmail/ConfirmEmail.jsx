import React, {useState} from "react";
import { View, Text, Image, StyleSheet, ScrollView} from "react-native";
import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from "../../../components/CustomerButton";
import { useNavigation } from "@react-navigation/native";

const ConfirmEmail = () => {
    const [code, setCode] = useState('');
    const navigation = useNavigation();

    const SignConfirmPressed = () => {
        console.warn("Sign Up");
        navigation.navigate("Sign Up");
    }

    const resendPressed = () => {
        console.warn("Resend code");
    }

    const loginPressed = () => {
        console.warn("Log in");
        navigation.navigate("Sign In");
    }

    return (
    <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.ConfirmEmailContainer}>
            <Text style={styles.ConfirmEmailTitle}>Confirmation your email</Text>
            <CustomerInput
            placeholder="Enter your confirmation code"
            value={code}
            setValue={setCode}
            secureTextEntry={false}
            />
            <CustomerButton text="Confirm" onPress={SignConfirmPressed} bgColor={""} fgColor={""}/>

            <CustomerButton
            text="Ressend"
            onPress={resendPressed}
            type="SECONDARY"
            bgColor={""}
            fgColor={""}
            />

            <CustomerButton
            text="Back to Sign in here"
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
    ConfirmEmailContainer: {
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
    ConfirmEmailTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#051C60',
        margin: 10,
    },
})

export default ConfirmEmail;