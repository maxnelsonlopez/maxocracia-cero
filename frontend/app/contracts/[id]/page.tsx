import ContractDetailsClient from "./ContractDetailsClient";

export function generateStaticParams() {
  return [{ id: "placeholder" }];
}

export const dynamicParams = false;

export default function ContractDetailsPage() {
  return <ContractDetailsClient />;
}

