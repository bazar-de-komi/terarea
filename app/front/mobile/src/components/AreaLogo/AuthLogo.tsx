import React from "react";
import { View, Image, StyleSheet, useWindowDimensions} from "react-native";

import AreaLogo from '../../../assets/authenticationLogo/AreaLogo.png';

const AuthLogo = () => {
    const { height } = useWindowDimensions();

    return (
        <View>
            <Image
                source={AreaLogo}
                style={[styles.areaLogo, { height: height * 0.1 }]}
                resizeMode="contain"
            />
        </View>
    )
}

const styles = StyleSheet.create({
    areaLogo: {
        width: '40%',
        maxWidth: 300,
        maxHeight: 100,
        marginBottom: 60,
    },
})

export default AuthLogo

