import React from 'react';
import { WebView } from 'react-native-webview';
import { getValue } from '../../../components/StoreData/storeData';
import { queries } from '../../../../back-endConnection/querier';

const OAuthScreen = async () => {
    const authUrl = await getValue("authUrl")

    const onNavigationStateChange = async (event: any) => {
        if (event.url.startsWith("https://pringpal.news/callback")) {
            const urlParams = new URLSearchParams(event.url.split('?')[1]);
            const code = urlParams.get('code');
            if (code) {
                let path: string = "/api/v1/oauth/callback?";
                path += event.url.split('?')[1];
                console.log("Path:", path);
                const response = await queries.get(path);
                console.log("Response:", response)
                // Fermez la WebView ou redirigez l'utilisateur selon vos besoins
                // navigation.goBack();
                // Envoyer le code au backend ou gérer l'authentification
            };
        }
    };

    return (
        <WebView
            source={{ uri: authUrl }}
            onNavigationStateChange={onNavigationStateChange}
            startInLoadingState
        />
    );
};

export default OAuthScreen;
