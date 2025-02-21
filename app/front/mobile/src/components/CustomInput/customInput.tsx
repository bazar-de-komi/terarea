import React from "react";
import { View, TextInput, StyleSheet } from 'react-native'

const CustomInput = ({ value, setValue, placeholder, secureTextEntry }) => {
    return (
        <View style={styles.customInputContainer}>
            <TextInput
                value={value}
                onChangeText={setValue}
                placeholder={placeholder}
                secureTextEntry={secureTextEntry}
            />
        </View>
    )
}

const styles = StyleSheet.create({
    customInputContainer: {
        backgroundColor: 'white',
        width: '70%',
        height: 30,

        borderColor: '#e8e8e8',
        borderWidth: 1,
        borderRadius: 10,

        paddingHorizontal: 10,
        justifyContent: 'center',
        marginVertical: 5,
    }
})

// const styles = StyleSheet.create({
//     CustomInputContainer: {
//         backgroundColor: 'white',
//         width: '70%',
//         height: 26,

//         borderColor: '#e8e8e8',
//         borderRadius: 10,

//         paddingHorizontal: 10,
//         paddingTop: 4,
//         marginVertical: 5,
//     },
// })

export default CustomInput
