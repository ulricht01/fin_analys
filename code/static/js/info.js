var style = document.createElement('style');
style.innerHTML = `
.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 200px;
  color: #fff;
  text-align: center;
  position: absolute;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 12px;
}

.tooltip .tooltiptext::after {
  content: "";
  position: absolute;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
`;
document.head.appendChild(style);