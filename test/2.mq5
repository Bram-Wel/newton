//+------------------------------------------------------------------+
//|                                                    EvenOdd.mq5   |
//|                 Copyright 2023, MetaQuotes Software Corp.         |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright   "Copyright 2023, MetaQuotes Software Corp."
#property link        "https://www.mql5.com"
#property description "Even Odd"

#property indicator_separate_window
#property indicator_buffers 3
#property indicator_plots   1
#property indicator_type1   DRAW_LINE
#property indicator_color1  DodgerBlue
#property indicator_label1  "Even Odd (1-120)"
#property indicator_type2   DRAW_LINE
#property indicator_color2  MediumVioletRed
#property indicator_label2  "Even Odd (1-5000)"
#property indicator_type3   DRAW_LINE
#property indicator_color3  LimeGreen
#property indicator_label3  "Difference (%)"

//--- indicator buffers
double ExtEOBuffer1[];
double ExtEOBuffer2[];
double ExtDiffBuffer[];

//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
void OnInit()
{
    //--- indicator digits
    IndicatorSetInteger(INDICATOR_DIGITS, 0);

    //--- indicator short name
    IndicatorSetString(INDICATOR_SHORTNAME, "Even Odd");

    //--- index buffers
    SetIndexBuffer(0, ExtEOBuffer1);
    SetIndexBuffer(1, ExtEOBuffer2);
    SetIndexBuffer(2, ExtDiffBuffer);

    //--- set index draw begin
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 0);
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 0);
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, 0);
}

//+------------------------------------------------------------------+
//| Even Odd Calculation                                             |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                const int prev_calculated,
                const datetime &time[],
                const double &open[],
                const double &high[],
                const double &low[],
                const double &close[],
                const long &tick_volume[],
                const long &volume[],
                const int &spread[])
{
    //--- check for bars count
    if (rates_total < 1)
        return 0; // exit with zero result

    //--- get current position
    int pos = prev_calculated - 1;
    if (pos < 0)
        pos = 0;

    //--- calculate even/odd for each period
    for (int i = pos; i < rates_total && !IsStopped(); i++)
    {
        //--- determine if the bar is even or odd for period 1 to 120
        for (int period = 1; period <= 120; period++)
        {
            int eo = i % period;

            //--- store the result in the appropriate buffer
            if (period <= 120)
                ExtEOBuffer1[i] = eo;
        }

        //--- determine if the bar is even or odd for period 1 to 5000
        for (int period = 1; period <= 5000; period++)
        {
            int eo = i % period;

            //--- store the result in the appropriate buffer
            if (period <= 5000)
                ExtEOBuffer2[i] = eo;
        }

        //--- calculate the difference in percentage between the two sets of periods
        double diff = ((ExtEOBuffer2[i] - ExtEOBuffer1[i]) / ExtEOBuffer1[i]) * 100.0;
        ExtDiffBuffer[i] = diff;
    }

    return rates_total;
}
