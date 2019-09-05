declare module repositories {

    export interface User {
        name: string;
        image: string;
    }

    export interface Repository {
        categories: string[];
        keywords: string[];
        users: User[];
        name: string;
        abstract: string;
        uri: string;
    }

}
