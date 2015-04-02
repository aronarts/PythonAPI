#ifndef FILELOGGER_HPP
#define FILELOGGER_HPP

#include <fstream>

// Use the namespace you want
class FileLogger {

public:
	static FileLogger &Instance()
	{
		static FileLogger logger("c:\\Work\\Projects\\Example1\\log.txt");
		return logger;
	}



	// ctor (remove parameters if you don´t need them)
	explicit FileLogger(const char *fname = "log.txt")
		: numWarnings(0U),
		numErrors(0U)
	{

		myFile.open(fname);

		// Write the first lines
		if (myFile.is_open()) {
			myFile << "Log file created" << std::endl << std::endl;
		} // if

	}


	// dtor
	~FileLogger() {

		if (myFile.is_open()) {
			myFile << std::endl << std::endl;

			// Report number of errors and warnings
			myFile << numWarnings << " warnings" << std::endl;
			myFile << numErrors << " errors" << std::endl;

			myFile.close();
		} // if

	}


	// Overload << operator using C style strings
	// No need for std::string objects here
	friend FileLogger &operator << (FileLogger &logger, const char *text) {

		logger.myFile << text << std::endl;
		return logger;

	}


	// Make it Non Copyable (or you can inherit from sf::NonCopyable if you want)
	FileLogger(const FileLogger &) = delete;
	FileLogger &operator= (const FileLogger &) = delete;



private:

	std::ofstream           myFile;

	unsigned int            numWarnings;
	unsigned int            numErrors;

}; // class end


#endif // FILELOGGER_HPP