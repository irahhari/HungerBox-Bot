@echo off

echo           *    *  ******  *       ******  *******  *    *  ******              
echo           *    *  *       *       *       *     *  **  **  *                   
echo           * ** *  ******  *       *       *     *  * ** *  ******              
echo           **  **  *       *       *       *     *  *    *  *                   
echo           *    *  ******  ******  ******  *******  *    *  ******              
echo.
echo                               *******   *******                                
echo                                  *      *     *                                
echo                                  *      *     *                                
echo                                  *      *     *                                
echo                                  *      *******                                
echo.
echo *     *  *     *  *     *  ******  ******  *****   *****   *******  *      *   
echo *     *  *     *  * *   *  *       *       *    *  *    *  *     *    *  *     
echo *******  *     *  *  *  *  *  ***  ******  *****   *****   *     *     **      
echo *     *  *     *  *   * *  *    *  *       * *     *    *  *     *    *  *     
echo *     *  *******  *     *  ******  ******  *   *   *****   *******  *      *   
echo.
echo                            *****   *******  *******                            
echo                            *    *  *     *     *                               
echo                            *****   *     *     *                               
echo                            *    *  *     *     *                               
echo                            *****   *******     *                               

pause

echo Installing the packages

@REM gets date and formats it
set year=%date:~10,4%
set month=%date:~4,2%
set day=%date:~7,2%
set dateformatted=%day%-%month%-%year%

@REM finds the python path
for /f "delims=" %%F in ('where python') do set python=%%F

@REM installs and upgrades all the required packages
pip install -Ur ./config/packages.txt >> ./log/pip/pre_%dateformatted%.log 2>&1

cls

@REM runs the bot to book
%python% ./src/preference.py

@REM self-destructs this file
@REM start /b cmd /c del "%~f0"&exit /b