import { getFirestore, collection } from "firebase/firestore";
import { initializeApp } from 'firebase/app'

const firebaseApp = initializeApp({});

// used for the firestore refs
export const db = getFirestore(firebaseApp)
export const numbersRef = collection(db, "numbers");