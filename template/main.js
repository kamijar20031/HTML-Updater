const pages = [document.getElementById("page1"),document.getElementById("page2"), document.getElementById("page3")];
const numPages = pages.length;
const cards = document.getElementsByClassName("mainBoxes");
const cardPlaceholder = document.getElementById("placeholder");

var currentPage = 1;
var shuffled = false;
var waitingCard = false;
var waitingPage = false;
var changeThemeFlag = false;

var r = document.querySelector(':root');

var darkTheme = window.matchMedia("(prefers-color-scheme: dark)").matches;

if (darkTheme)
{
    document.getElementById("theme").children[0].classList.add("icon-sun")
    document.getElementById("theme").children[0].classList.remove("icon-moon")
}

function changeIMG(id)
{
    let img = document.getElementById(`images_${id}`);
    let idx = (images[id].idx+1)%(images[id].srcs.length);
    let src = images[id].srcs[idx];
    img.style.animationName = "imgChangeIn";
    setTimeout(() => {
        img.src = src;
        img.style.animationName = "imgChangeOut";
    }, 500)
    images[id].idx = idx;
}

function changeThemeInner()
{
    if (!changeThemeFlag) 
        {
            changeThemeFlag = true;
            if (darkTheme) 
            {
                r.style.colorScheme = "light";
                document.getElementById("theme").children[0].classList.add("icon-moon")
                document.getElementById("theme").children[0].classList.remove("icon-sun")
            }
            else 
            {
                r.style.colorScheme = "dark";
                document.getElementById("theme").children[0].classList.add("icon-sun")
                document.getElementById("theme").children[0].classList.remove("icon-moon")
            }
            setTimeout(() => {
                changeThemeFlag = false;
            }, 500)
            darkTheme = !darkTheme;
        }
}

function changeTheme()
{
    if (!document.startViewTransition)
        changeThemeInner();
    else
        document.startViewTransition(() => {
            changeThemeInner();
        });

}

function nextPage()
{
    
    if (currentPage<numPages && !waitingPage)
    {
        waitingPage = true;
        pages[currentPage].style.animationName = "scrollUp";
        pages[currentPage].addEventListener('animationend', () => {
            waitingPage=false;
        }, { once: true });
        currentPage++;
    }
}
function prevPage()
{
    
    if (currentPage>1  && !waitingPage)
    {
        waitingPage = true;
        currentPage--;
        pages[currentPage].style.animationName = "scrollDown";
        pages[currentPage].addEventListener('animationend', () => {
            waitingPage=false;
        }, { once: true });
        
    }
}

function changeIntroCard()
{
    if (!waitingCard)
    {
        waitingCard = true;
        shuffled = !shuffled;
        cards[+shuffled].childNodes[1].style.animationName = "cardToBack";
        cards[+(!shuffled)].childNodes[1].style.animationName = "cardToFront";
        cards[+shuffled].childNodes[1].addEventListener('animationend', () => {
            waitingCard=false;
        });
    }
}

cardPlaceholder.addEventListener("mouseenter", changeIntroCard);