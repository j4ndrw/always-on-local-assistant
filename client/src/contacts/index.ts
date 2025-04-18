import { Contacts } from "@capacitor-community/contacts";

export const getContacts = async () => {
  const payload = await Contacts.getContacts({
    projection: { name: true, phones: true },
  });
  return payload.contacts.reduce(
    (acc, contact) => {
      const name = contact.name?.display ?? "";
      const [phone] = contact.phones?.map(({ number }) => number) ?? [];
      if (!name || !phone) return acc;
      acc[name] = phone;
      return acc;
    },
    {} as Record<string, string>,
  );
};
