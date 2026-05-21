async function runWorkflow() {

    document.getElementById("logs").innerHTML =
        "⏳ Running AI Agents...";

    const response = await fetch("/run");

    const data = await response.json();

    document.getElementById("research").innerText =
        data.research;

    document.getElementById("website").innerText =
        data.website;

    document.getElementById("marketing").innerText =
        data.marketing;

    document.getElementById("finance").innerText =
        data.finance;

    document.getElementById("logs").innerHTML =
        data.logs.join("<br>");
}