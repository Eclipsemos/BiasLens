from cfg import LLM_API_KEY, LLM_MODEL_NAME
from biaslens import BiasLens




if __name__ == "__main__":
    # Example usage

    sample_request = {
        "page_gross_text": """https://www.newsmax.com/danielmccarthy/pope-francis-catholicism/2025/04/23/id/1208016/
        After Francis, Catholics Need a Populist Pope\nBy Daniel McCarthy Wednesday, 23 April 2025 12:04 PM EDT
        But even as Francis took a gentle approach to those who insisted the church "modernize," he cracked down hard on those in the West who were drawn to Catholicism precisely for its traditionalism, particularly those who wished to attend the Latin Mass.
        pope francis at mass holding up a large silver cup
        Pope Francis was meant to be a pontiff for the age of globalization.
        The pope's spiritual mission doesn't change, but its earthly context does, and when the College of Cardinals chose Argentina's Jorge Maria Bergoglio as successor to the retiring Pope Benedict XVI, they made a guess about where the world was going.
        They proved to be wrong.
        In 2013, when Bergoglio became Pope Francis, same-sex marriage was rapidly gaining acceptance in America and Europe, but no one was yet talking about "pronouns" or what transgender ideology would mean for women's sports and children's bodies.
        Barack Obama had just been reelected as America's president, heralding, in the eyes of hopeful supporters, a post-racial epoch not only in our politics but perhaps everywhere.
        The political consensus on both sides of the Atlantic favored free trade and high levels of immigration — the question was only how high.
        The entire planet would soon be a single community, and all that remained to do was reconcile the United States and Europe with the global South.
        That called for reminding wealthy Americans and Europeans of their duties to the world's poor: Francis wasn't picked to be a socialist pope, but one who would provide a moral counterpoint to the cold logic of economic globalization.
        The cardinals also wanted Francis to strike a balance between north and south in the politics of sex and sexuality.
        With same-sex marriage triumphant, the Catholic Church seemed to be on the losing side of the West's culture war, with its future dependent on negotiating the best possible terms of surrender.
        The church couldn't simply repudiate its teachings on homosexuality, contraception or the ordination of women — it recognized those as God's own teachings, after all, and if the Western public might have been content to dispense with them, people in the places where Christianity was growing, not shrinking, such as Africa, were not.
        Catholics saw what was happening to the Anglican Communion and many mainline Protestant denominations, which were ripped apart by divisions over homosexuality and the role of women in the church, with permanent rifts splitting African and Western congregations.
        Francis was meant to bridge the Catholic Church's factions.
        He would — and did — uphold the church's core teachings, yet he'd present them in ways designed to reassure dissenters and progressives of their place in the flock.
        But even as Francis took a gentle approach to those who insisted the church "modernize," he cracked down hard on those in the West who were drawn to Catholicism precisely for its traditionalism, particularly those who wished to attend the Latin Mass.
        What neither Francis nor the cardinals who elected him anticipated was that massive political conflict over globalization was about to erupt in the West itself, just as progressives' promotion of gender ideology was about to give the Right the upper hand in the culture war.
        Francis envisioned a socially moderate church that would accommodate liberal Western attitudes — without capitulating entirely to them — while appealing to the global South with criticisms of the capitalist world economy.
        Yet now the church has an unexpected opportunity to evangelize the West anew using the opposite strategy, if the cardinals select a pope as different from Francis as Francis was from the conservative Benedict XVI.
        For despite Francis' hostility, the Latin Mass has continued to pull new converts and lapsed Catholics into the pews.
        And recent polling shows the decline of Christianity in America and Europe has slowed, halted, or even, in places, reversed:
        Young men in particular are becoming more religious, a trend connected to a rightward turn in politics.
        In France, the church has just recorded a 45% increase over last year in adult baptisms at Easter — leading to the largest number of converts entering the church this season in the 20 years the French Bishops' Conference has been conducting its survey.
        On the last day of his life, Pope Francis met with Vice President JD Vance, a young Catholic convert on the populist right who exemplifies the changes taking place in the world and Church alike.
        The next pope may be as critical of Trump-Vance immigration policy as Francis was; a pope can be expected to prioritize compassion, including for illegal immigrants.
        But if Francis was the pope for a globalist era, what the Catholic Church needs now is a populist pope, one who understands that if the church renews its ties to the working class within the West, not just in the global South, it will find ready converts.
        Likewise, a church that emphasizes traditional moral teachings in Europe and America, as well as Africa, will grow.
        Pope Francis was too conservative, too much a man of his time, in one sense — he didn't go far enough in recognizing the upheavals of globalism and the attraction of traditionalism even in the wealthiest parts of the world.
        Daniel McCarthy, a recognized expert on conservative thought, is the editor-in-chief of Modern Age: A Conservative Review. He's also a regular contributor to The Spectator's World edition. He has a long association with The American Conservative, a magazine co-founded by Pat Buchanan. Mr. McCarthy's writings appeared in a variety of publications. He has appeared on PBS NewsHour, NPR, the BBC, the Australian Broadcasting Corporation, CNN International and other radio and television outlets. Read more of Daniel McCarthy's reports — Here."""
    }

    lens = BiasLens(sample_request, LLM_API_KEY, LLM_MODEL_NAME)
    lens.article_pre_analysis()

    print(lens.results)