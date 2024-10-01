import React, {useState} from "react";
import { View, Text, Image, StyleSheet, ScrollView} from "react-native";
import CustomerInput from "../../../components/CustomersInput/CustomerInput";
import CustomerButton from "../../../components/CustomerButton";
import { useNavigation } from "@react-navigation/native";

const ForgotPassword = () => {
    const [email, setEmail] = useState('');
    const navigation = useNavigation();

    const SignSendPressed = () => {
        console.warn("send");
    }

    const loginPressed = () => {
        console.warn("Log in");
        navigation.navigate("Sign In");
    }

    return (
    <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.ForgotPasswordContainer}>
            <Text style={styles.ForgotPasswordTitle}>Reset your password</Text>
            <CustomerInput
            placeholder="email"
            value={email}
            setValue={setEmail}
            secureTextEntry={false}
            />
            <CustomerButton
            text="Send"
            onPress={SignSendPressed}
            bgColor={""}
            fgColor={""}
            />
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
    ForgotPasswordContainer: {
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
    ForgotPasswordTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#051C60',
        margin: 10,
    },
})

export default ForgotPassword;